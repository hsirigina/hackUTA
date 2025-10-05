#!/usr/bin/env python3
"""
Force connect to Arduino using its MAC address, even if not advertising
"""
import asyncio
from bleak import BleakClient, BleakScanner

# The address we found earlier
ARDUINO_ADDRESS = "642B8DC2-D778-8A47-20C2-B91C64716DBF"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-cba987654321"

class DrivingMonitor:
    def __init__(self):
        self.event_count = 0
        
    def process_data(self, message):
        """Process incoming driving data"""
        try:
            if message.startswith("EVENT:"):
                parts = message.split(":")
                event_type = parts[1]
                count = int(parts[2])
                self.event_count = count
                print(f"🚨 EVENT: {event_type} (Total: {count})")
                
            elif message.startswith("STATUS:"):
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
                    
                    import time
                    if event_type != "" or int(time.time()) % 10 == 0:
                        print(f"Sensors: X={ax:.2f}, Y={ay:.2f}, Z={az:.2f} | Event: {event_type} | Count: {count}")
                        
        except Exception as e:
            print(f"Error processing data: {e}")

async def main():
    monitor = DrivingMonitor()
    
    print("🔧 Attempting DIRECT connection to Arduino...")
    print(f"Address: {ARDUINO_ADDRESS}")
    print("(This will work even if Arduino is already 'connected')")
    print()
    
    try:
        async with BleakClient(ARDUINO_ADDRESS, timeout=15.0) as client:
            print("✅ Connected to Driving Monitor!")
            print("📱 Receiving driving data...")
            print("Press Ctrl+C to disconnect")
            print("-" * 50)
            
            def notification_handler(sender, data):
                message = data.decode('utf-8')
                monitor.process_data(message)
            
            # Subscribe to notifications
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n📊 Summary:")
                print(f"Total aggressive events: {monitor.event_count}")
                print("Disconnected!")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Try these solutions:")
        print("1. Unplug and replug the Arduino")
        print("2. Turn Bluetooth OFF and ON on your Mac")
        print("3. Press the reset button on the Arduino")
        print("4. Check Arduino Serial Monitor - it should show 'Advertising'")

if __name__ == "__main__":
    asyncio.run(main())
