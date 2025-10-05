import asyncio
import time
from datetime import datetime, timezone
from bleak import BleakClient, BleakScanner
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import sys

# Force unbuffered output so logs show in real-time
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load environment variables
load_dotenv()

class SupabaseDrivingMonitor:
    def __init__(self, arduino_id: str = "ARD-001"):
        self.arduino_id = arduino_id
        self.event_count = 0
        self.last_event_time = 0
        self.aggressive_events = []
        self.session_id = None
        self.driver_id = None
        self.heartbeat_task = None
        self.session_timeout_task = None

        # Track last event timestamp for each event type (time-based cooldown)
        self.last_event_timestamps = {
            'SWERVING': 0,
            'HARSH_BRAKE': 0,
            'AGGRESSIVE': 0
        }

        # Cooldown period in seconds - same event type must wait this long before saving again
        self.EVENT_COOLDOWN_SECONDS = 3.0

        # Track last score update time for gradual recovery
        self.last_score_recovery_time = time.time()

        # Initialize Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for backend operations

        if not supabase_url or not supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file")

        self.supabase: Client = create_client(supabase_url, supabase_key)
        print(f"✅ Connected to Supabase")

    async def initialize_session(self):
        """Find or create driver and start a new driving session"""
        try:
            # Find driver by Arduino ID
            response = self.supabase.table('drivers').select('*').eq('arduino_id', self.arduino_id).execute()

            if not response.data:
                print(f"❌ Driver not found for Arduino ID: {self.arduino_id}")
                print("Please create a driver in Supabase first or use an existing Arduino ID")
                return False

            driver = response.data[0]
            self.driver_id = driver['id']
            print(f"✅ Found driver: {driver['name']} ({driver['email']})")

            # Create new driving session with default 100 safety score
            session_data = {
                'driver_id': self.driver_id,
                'arduino_id': self.arduino_id,
                'status': 'active',
                'safety_score': 100,
                'started_at': datetime.now(timezone.utc).isoformat()
            }

            session_response = self.supabase.table('driving_sessions').insert(session_data).execute()
            self.session_id = session_response.data[0]['id']
            print(f"✅ Started new driving session: {self.session_id}")

            # Update driver status to active and online
            self.supabase.table('drivers').update({
                'status': 'active',
                'connection_status': 'online',
                'last_active': datetime.now(timezone.utc).isoformat(),
                'last_heartbeat': datetime.now(timezone.utc).isoformat()
            }).eq('id', self.driver_id).execute()

            print(f"🟢 Driver is now ONLINE")

            # Send email notification to supervisor
            self.send_supervisor_notification()

            # Start heartbeat, score recovery, and timeout tasks
            self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            self.score_recovery_task = asyncio.create_task(self.score_recovery_loop())
            self.session_timeout_task = asyncio.create_task(self.session_timeout_monitor())

            return True

        except Exception as e:
            print(f"❌ Error initializing session: {e}")
            return False

    async def heartbeat_loop(self):
        """Send heartbeat every 10 seconds to show driver is online"""
        try:
            while True:
                await asyncio.sleep(10)
                self.supabase.table('drivers').update({
                    'last_heartbeat': datetime.now(timezone.utc).isoformat()
                }).eq('id', self.driver_id).execute()
        except asyncio.CancelledError:
            print("Heartbeat stopped")

    def send_supervisor_notification(self):
        """Send email notification to supervisor when driver goes online"""
        try:
            import subprocess
            print(f"📧 Sending supervisor notification for driver {self.driver_id}...")

            # Run notification script in background
            subprocess.Popen(
                [sys.executable, 'notify_supervisor.py', self.driver_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("   ✓ Notification triggered")
        except Exception as e:
            print(f"   ⚠️  Could not send notification: {e}")

    async def score_recovery_loop(self):
        """Check for score recovery every 5 seconds during safe driving"""
        try:
            while True:
                await asyncio.sleep(5)
                # Check if we should recover points (no penalty)
                print("🔍 Checking for score recovery...")
                await self.update_session_score(penalty_points=0)
        except asyncio.CancelledError:
            print("Score recovery stopped")

    async def session_timeout_monitor(self):
        """Auto-end session after 5 minutes of inactivity"""
        try:
            while True:
                await asyncio.sleep(60)  # Check every minute

                # Get last heartbeat time
                driver = self.supabase.table('drivers').select('last_heartbeat').eq('id', self.driver_id).execute()
                if driver.data:
                    last_heartbeat = datetime.fromisoformat(driver.data[0]['last_heartbeat'].replace('Z', '+00:00'))
                    time_since_heartbeat = (datetime.now(last_heartbeat.tzinfo) - last_heartbeat).total_seconds()

                    # If no heartbeat for 5 minutes, end session
                    if time_since_heartbeat > 300:  # 5 minutes
                        print("⏱️  No activity for 5 minutes, ending session...")
                        await self.end_session()
                        break
        except asyncio.CancelledError:
            print("Timeout monitor stopped")

    def calculate_severity(self, event_type: str, x: float, y: float, z: float) -> str:
        """Calculate severity based on event type and sensor values"""
        magnitude = (x**2 + y**2 + z**2) ** 0.5

        if event_type == "HARSH_BRAKE":
            return 'high' if magnitude > 2.0 else 'medium'
        elif event_type == "AGGRESSIVE":
            return 'high'
        elif event_type == "SWERVING":
            return 'medium' if magnitude > 1.5 else 'low'
        else:
            return 'low'

    async def save_sensor_reading(self, x: float, y: float, z: float, event_type: str, count: int):
        """Save raw sensor reading to Supabase - ONLY when there's an event"""
        try:
            # Only save sensor readings if there's an actual event
            if not event_type or event_type not in ['SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE']:
                return

            sensor_data = {
                'session_id': self.session_id,
                'arduino_id': self.arduino_id,
                'x': x,
                'y': y,
                'z': z,
                'event_type': event_type,
                'count_at_time': count,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

            self.supabase.table('sensor_readings').insert(sensor_data).execute()

        except Exception as e:
            print(f"⚠️  Error saving sensor reading: {e}")

    async def save_event(self, event_type: str, x: float, y: float, z: float, count: int):
        """Save driving event to Supabase"""
        try:
            severity = self.calculate_severity(event_type, x, y, z)

            event_data = {
                'session_id': self.session_id,
                'driver_id': self.driver_id,
                'arduino_id': self.arduino_id,
                'event_type': event_type,
                'x': x,
                'y': y,
                'z': z,
                'count_at_time': count,
                'severity': severity,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

            self.supabase.table('events').insert(event_data).execute()

            # Calculate penalty points based on event type (doubled for faster demo)
            penalty_points = {
                'AGGRESSIVE': 10,
                'HARSH_BRAKE': 6,
                'SWERVING': 2
            }.get(event_type, 0)

            print(f"💾 {event_type} event (Severity: {severity}) | Safety score -{penalty_points}")

            # Update safety score with penalty
            await self.update_session_score(penalty_points=penalty_points)

            # Update driver status based on event count
            if count >= 5:
                self.supabase.table('drivers').update({
                    'status': 'warning'
                }).eq('id', self.driver_id).execute()

        except Exception as e:
            print(f"⚠️  Error saving event: {e}")

    async def update_session_score(self, penalty_points=0):
        """Update safety score for current session

        Args:
            penalty_points: Points to deduct (0 for recovery check only)
        """
        try:
            # Get current session
            session = self.supabase.table('driving_sessions').select('*').eq('id', self.session_id).execute()

            if session.data:
                session_data = session.data[0]
                current_score = session_data.get('safety_score', 100)

                # Apply penalty if event occurred
                if penalty_points > 0:
                    current_score -= penalty_points
                    self.last_score_recovery_time = time.time()  # Reset recovery timer
                else:
                    # Check MOST RECENT event from BOTH BLE and attention monitoring
                    recent_events = self.supabase.table('events').select('timestamp').eq('session_id', self.session_id).order('timestamp', desc=True).limit(1).execute()

                    if recent_events.data:
                        # Get time since last event (from ANY source - driving or attention)
                        last_event_timestamp = datetime.fromisoformat(recent_events.data[0]['timestamp'].replace('Z', '+00:00'))
                        time_since_last_event = (datetime.now(timezone.utc) - last_event_timestamp).total_seconds()

                        print(f"   Time since LAST EVENT (any type): {time_since_last_event:.1f}s | Current score: {current_score}")

                        if time_since_last_event >= 5:
                            recovery_cycles = int(time_since_last_event / 5)
                            recovery_points = recovery_cycles * 2  # 2 points per 5 seconds
                            new_score = min(100, current_score + recovery_points)
                            current_score = new_score
                            if recovery_points > 0:
                                print(f"✨ Good driving! Safety score +{recovery_points} → {current_score}")
                        else:
                            print(f"   Not enough time passed for recovery (need 5s, have {time_since_last_event:.1f}s)")
                    else:
                        # No events yet, use time since session start
                        time_since_recovery = time.time() - self.last_score_recovery_time
                        if time_since_recovery >= 5:
                            recovery_points = int(time_since_recovery / 5) * 2  # 2 points per 5 seconds
                            current_score = min(100, current_score + recovery_points)
                            if recovery_points > 0:
                                print(f"✨ Good driving! Safety score +{recovery_points} → {current_score}")

                # Clamp score between 0 and 100
                current_score = max(0, min(100, current_score))

                # Update session
                self.supabase.table('driving_sessions').update({
                    'safety_score': current_score
                }).eq('id', self.session_id).execute()

                # Update driver's overall safety score
                self.supabase.table('drivers').update({
                    'safety_score': current_score,
                    'last_active': datetime.now(timezone.utc).isoformat()
                }).eq('id', self.driver_id).execute()

        except Exception as e:
            print(f"⚠️  Error updating session score: {e}")

    async def process_data(self, message: str):
        """Process incoming driving data and save to Supabase"""
        try:
            if message.startswith("EVENT:"):
                # Event notification: EVENT:HARSH_BRAKE:3
                parts = message.split(":")
                event_type = parts[1]
                count = int(parts[2])
                self.event_count = count
                self.last_event_time = time.time()
                self.aggressive_events.append({
                    'type': event_type,
                    'time': time.strftime('%H:%M:%S'),
                    'count': count
                })
                print(f"🚨 EVENT: {event_type} (Total: {count})")

            elif message.startswith("STATUS:"):
                # Status update: STATUS:AGGRESSIVE:3
                parts = message.split(":")
                status = parts[1]
                count = int(parts[2])
                print(f"📊 STATUS: {status} driving (Events: {count})")

                # Check for score recovery (no penalty)
                await self.update_session_score(penalty_points=0)

            else:
                # Raw sensor data: ax,ay,az,event_type,count
                parts = message.split(",")
                if len(parts) >= 5:
                    x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                    event_type = parts[3].strip()
                    count = int(parts[4])

                    # Only process if there's an actual event
                    if event_type and event_type in ['SWERVING', 'HARSH_BRAKE', 'AGGRESSIVE']:
                        current_time = time.time()
                        time_since_last_event = current_time - self.last_event_timestamps[event_type]

                        # Only save if cooldown period has passed (prevents duplicate events)
                        if time_since_last_event >= self.EVENT_COOLDOWN_SECONDS:
                            # Update the last event timestamp
                            self.last_event_timestamps[event_type] = current_time

                            # Save sensor reading with event data
                            await self.save_sensor_reading(x, y, z, event_type, count)

                            # Save the event
                            await self.save_event(event_type, x, y, z, count)

                            # Print event
                            print(f"🎯 {event_type}: X={x:.2f}, Y={y:.2f}, Z={z:.2f} (cooldown: {time_since_last_event:.1f}s)")

        except Exception as e:
            print(f"Error processing data: {e}")

    async def end_session(self):
        """End the current driving session"""
        try:
            print("\n🛑 Ending session and setting driver offline...")

            # Cancel background tasks
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
                print("   ✓ Heartbeat stopped")
            if hasattr(self, 'score_recovery_task') and self.score_recovery_task:
                self.score_recovery_task.cancel()
                print("   ✓ Score recovery stopped")
            if self.session_timeout_task:
                self.session_timeout_task.cancel()
                print("   ✓ Timeout monitor stopped")

            if self.session_id:
                # Update session status
                self.supabase.table('driving_sessions').update({
                    'status': 'completed',
                    'ended_at': datetime.now(timezone.utc).isoformat()
                }).eq('id', self.session_id).execute()
                print(f"   ✓ Session completed: {self.session_id}")

                # Update driver status to inactive and offline
                result = self.supabase.table('drivers').update({
                    'status': 'inactive',
                    'connection_status': 'offline'
                }).eq('id', self.driver_id).execute()
                print(f"   ✓ Driver set to OFFLINE: {self.driver_id}")
                print(f"   ✓ Database update result: {result.data}")

                print(f"\n✅ Session ended successfully")
                print(f"🔴 Driver is now OFFLINE")

        except Exception as e:
            print(f"⚠️  Error ending session: {e}")


async def main():
    # Use the Bluetooth address as Arduino ID
    arduino_id = "642B8DC2-D778-8A47-20C2-B91C64716DBF"
    print(f"Using Arduino ID: {arduino_id}")

    monitor = SupabaseDrivingMonitor(arduino_id=arduino_id)

    # Initialize session
    if not await monitor.initialize_session():
        return

    # Connect directly to the known Arduino address
    print(f"\n🔍 Connecting to Arduino...")
    driving_monitor_address = arduino_id  # The address IS the arduino_id now

    try:
        async with BleakClient(driving_monitor_address) as client:
            print("✅ Connected to Driving Monitor!")
            print("📱 Receiving driving data and syncing to Supabase...")
            print("Press Ctrl+C to disconnect")
            print("-" * 50)

            def notification_handler(sender, data):
                message = data.decode('utf-8')
                asyncio.create_task(monitor.process_data(message))

            await client.start_notify("87654321-4321-4321-4321-cba987654321", notification_handler)

            try:
                while True:
                    await asyncio.sleep(1)
            except (KeyboardInterrupt, asyncio.CancelledError):
                pass  # Handle gracefully
            finally:
                # Always end session when exiting loop
                print("\n📊 Summary:")
                print(f"Total aggressive events: {monitor.event_count}")
                if monitor.aggressive_events:
                    print("Recent events:")
                    for event in monitor.aggressive_events[-5:]:  # Last 5 events
                        print(f"  - {event['time']}: {event['type']}")

                await monitor.end_session()
                print("Disconnected!")

    except (KeyboardInterrupt, asyncio.CancelledError):
        # Handle Ctrl+C at outer level
        print("\n⚠️  Interrupted - ending session...")
        await monitor.end_session()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        await monitor.end_session()

if __name__ == "__main__":
    asyncio.run(main())
