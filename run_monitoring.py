#!/usr/bin/env python3
"""
Master Monitoring Script
Runs both Arduino BLE monitoring and Attention monitoring simultaneously
"""
import asyncio
import subprocess
import sys
import signal
import os

class MonitoringManager:
    def __init__(self):
        self.ble_process = None
        self.attention_process = None
        self.running = True

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Stopping all monitoring processes...")
        self.running = False

        if self.ble_process:
            print("   Stopping BLE monitoring...")
            # Send SIGINT (Ctrl+C) instead of SIGTERM so scripts can cleanup
            import signal as sig_module
            self.ble_process.send_signal(sig_module.SIGINT)
            self.ble_process.wait(timeout=5)
            print("   ✓ BLE monitoring stopped")

        if self.attention_process:
            print("   Stopping attention monitoring...")
            self.attention_process.send_signal(sig_module.SIGINT)
            self.attention_process.wait(timeout=5)
            print("   ✓ Attention monitoring stopped")

        # Run cleanup to ensure driver is set offline
        self.cleanup_sessions()

        print("\n✅ All processes stopped successfully")
        sys.exit(0)

    def cleanup_sessions(self):
        """Ensure all sessions are closed and driver is offline"""
        try:
            from supabase import create_client
            from dotenv import load_dotenv
            from datetime import datetime, timezone
            import os

            load_dotenv()
            supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))

            driver_id = 'b52c0e82-8edf-4049-9696-fd4b9fcffc7c'

            # Close any active sessions
            active = supabase.table('driving_sessions').select('*').eq('driver_id', driver_id).eq('status', 'active').execute()

            if active.data:
                print(f"   🧹 Cleaning up {len(active.data)} active session(s)...")
                for session in active.data:
                    supabase.table('driving_sessions').update({
                        'status': 'completed',
                        'ended_at': datetime.now(timezone.utc).isoformat()
                    }).eq('id', session['id']).execute()

            # Set driver offline
            supabase.table('drivers').update({
                'connection_status': 'offline'
            }).eq('id', driver_id).execute()

            print("   ✓ Sessions closed and driver set offline")
        except Exception as e:
            print(f"   ⚠️  Cleanup warning: {e}")

    def run(self):
        """Start both monitoring processes"""
        print("\n" + "="*60)
        print("🚗 DRIVER MONITORING SYSTEM")
        print("="*60)
        print("\nStarting monitoring processes...")
        print("Press Ctrl+C to stop all monitoring\n")

        # Set up signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        try:
            # Start BLE monitoring in background
            print("🔵 Starting Arduino BLE monitoring...")
            self.ble_process = subprocess.Popen(
                [sys.executable, 'ble_supabase.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            print("   ✓ BLE monitoring started (PID: {})".format(self.ble_process.pid))

            # Wait a bit for session to be created
            print("\n⏳ Waiting 3 seconds for session initialization...")
            import time
            time.sleep(3)

            # Start attention monitoring
            print("\n👁️ Starting attention monitoring...")
            try:
                self.attention_process = subprocess.Popen(
                    [sys.executable, 'attention_supabase.py'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                print("   ✓ Attention monitoring started (PID: {})".format(self.attention_process.pid))

                # Wait a moment to see if it crashes immediately due to no camera
                time.sleep(2)
                if self.attention_process.poll() is not None:
                    # Process ended - likely no camera
                    print("   ⚠️  Attention monitoring failed to start (camera not available)")
                    print("   ℹ️  Continuing with BLE monitoring only...")
                    print("\n   💡 To enable attention monitoring:")
                    print("      1. Connect iPhone via Continuity Camera")
                    print("      2. Or ensure Mac camera is available")
                    print("      3. Then restart: python3 run_monitoring.py")
                    self.attention_process = None
            except Exception as e:
                print(f"   ⚠️  Could not start attention monitoring: {e}")
                print("   ℹ️  Continuing with BLE monitoring only...")
                self.attention_process = None

            print("\n" + "="*60)
            if self.attention_process:
                print("✅ ALL MONITORING ACTIVE (BLE + Camera)")
            else:
                print("✅ BLE MONITORING ACTIVE (Camera disabled)")
            print("="*60)
            print("\n📊 Monitoring Output:")
            print("-"*60 + "\n")

            # Monitor both processes and display output
            while self.running:
                # Check if BLE process ended - if so, kill everything
                if self.ble_process.poll() is not None:
                    print("\n⚠️  BLE monitoring process ended")
                    print("   🛑 Stopping all processes...")

                    # Kill attention process if running
                    if self.attention_process:
                        import signal as sig_module
                        self.attention_process.send_signal(sig_module.SIGINT)
                        self.attention_process.wait(timeout=5)

                    # Cleanup sessions
                    self.cleanup_sessions()
                    break

                # Check if attention process ended - if so, kill everything
                if self.attention_process and self.attention_process.poll() is not None:
                    print("\n⚠️  Attention monitoring process ended")
                    print("   🛑 Stopping all processes...")

                    # Kill BLE process
                    if self.ble_process:
                        import signal as sig_module
                        self.ble_process.send_signal(sig_module.SIGINT)
                        self.ble_process.wait(timeout=5)

                    # Cleanup sessions
                    self.cleanup_sessions()
                    break

                # Read output from BLE process
                if self.ble_process.stdout:
                    ble_line = self.ble_process.stdout.readline()
                    if ble_line:
                        print(f"[BLE] {ble_line}", end='')

                # Read output from attention process
                if self.attention_process and self.attention_process.stdout:
                    attention_line = self.attention_process.stdout.readline()
                    if attention_line:
                        print(f"[CAM] {attention_line}", end='')

                time.sleep(0.1)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.signal_handler(None, None)

def main():
    manager = MonitoringManager()
    manager.run()

if __name__ == "__main__":
    main()
