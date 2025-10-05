#!/usr/bin/env python3
"""Quick BLE scanner to detect nearby devices"""
import asyncio
from bleak import BleakScanner

async def scan():
    print("🔍 Scanning for BLE devices...")
    print("(This may take 5-10 seconds)\n")
    
    devices = await BleakScanner.discover(timeout=10.0)
    
    print(f"Found {len(devices)} device(s):\n")
    
    arduino_found = False
    for i, device in enumerate(devices, 1):
        name = device.name if device.name else "(Unknown)"
        print(f"{i}. {name}")
        print(f"   Address: {device.address}")
        print()
        
        if name != "(Unknown)" and ("Driving Monitor" in name or "Arduino" in name):
            arduino_found = True
            print("   ⭐ THIS IS YOUR ARDUINO! ⭐\n")
    
    if not arduino_found:
        print("❌ Arduino 'Driving Monitor' not found!")
        print("\nThis means you need to upload the Arduino code first.")
        print("Your Arduino needs to be programmed with 'driving_monitor.ino'")
    else:
        print("✅ Arduino is already programmed and ready!")
        print("You can run 'python3 ble.py' to start receiving data!")

if __name__ == "__main__":
    asyncio.run(scan())
