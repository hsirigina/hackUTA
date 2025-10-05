import asyncio
import time
from bleak import BleakClient, BleakScanner

class DrivingMonitor:
    def __init__(self):
        self.event_count = 0
        self.last_event_time = 0
        self.aggressive_events = []
        
    def process_data(self, message):
        """Process incoming driving data"""
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
                
            else:
                # Raw sensor data: ax,ay,az,event_type,count
                parts = message.split(",")
                if len(parts) >= 5:
                    ax, ay, az = float(parts[0]), float(parts[1]), float(parts[2])
                    event_type = parts[3]
                    count = int(parts[4])
                    
                    # Only print if there's an event or every 10 seconds
                    if event_type != "" or int(time.time()) % 10 == 0:
                        print(f"Sensors: X={ax:.2f}, Y={ay:.2f}, Z={az:.2f} | Event: {event_type} | Count: {count}")
                        
        except Exception as e:
            print(f"Error processing data: {e}")

async def main():
    monitor = DrivingMonitor()
    
    print("🔍 Looking for 'Driving Monitor' device...")
    print("Make sure your Arduino is running and advertising!")
    
    # First scan for the device
    print("Scanning for devices...")
    devices = await BleakScanner.discover(timeout=5.0)
    
    driving_monitor = None
    for device in devices:
        if device.name and ("Driving Monitor" in device.name or "Arduino" in device.name):
            driving_monitor = device
            break
    
    if not driving_monitor:
        print("❌ Driving Monitor not found!")
        print("Make sure:")
        print("1. Arduino is powered on")
        print("2. BLE code is uploaded")
        print("3. Arduino is advertising")
        return
    
    print(f"✅ Found Driving Monitor at: {driving_monitor.address}")
    
    try:
        async with BleakClient(driving_monitor.address) as client:
            print("✅ Connected to Driving Monitor!")
            print("📱 Receiving driving data...")
            print("Press Ctrl+C to disconnect")
            print("-" * 50)
            
            def notification_handler(sender, data):
                message = data.decode('utf-8')
                monitor.process_data(message)
            
            await client.start_notify("87654321-4321-4321-4321-cba987654321", notification_handler)
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n📊 Summary:")
                print(f"Total aggressive events: {monitor.event_count}")
                if monitor.aggressive_events:
                    print("Recent events:")
                    for event in monitor.aggressive_events[-5:]:  # Last 5 events
                        print(f"  - {event['time']}: {event['type']}")
                print("Disconnected!")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Make sure:")
        print("1. Arduino is powered on")
        print("2. BLE is advertising")
        print("3. Device name is 'Driving Monitor'")

if __name__ == "__main__":
    asyncio.run(main())