#!/usr/bin/env python3
"""
Automatically identifies which Bluetooth device is the Arduino
by checking for the driving monitor characteristic
"""
import asyncio
from bleak import BleakScanner, BleakClient

TARGET_CHARACTERISTIC = "87654321-4321-4321-4321-cba987654321"

async def test_device(device):
    """Test if a device is the Arduino by checking for our characteristic"""
    try:
        async with BleakClient(device.address, timeout=3.0) as client:
            if not client.is_connected:
                return False

            # Check services for our characteristic
            for service in client.services:
                for char in service.characteristics:
                    if str(char.uuid).lower() == TARGET_CHARACTERISTIC.lower():
                        return True
            return False
    except Exception as e:
        return False

async def find_arduino():
    print("\n" + "="*70)
    print("🔍 AUTOMATIC ARDUINO IDENTIFIER")
    print("="*70)
    print("\nScanning for Bluetooth devices...\n")

    devices = await BleakScanner.discover(timeout=10.0)

    unnamed_devices = [d for d in devices if not d.name or d.name == "Unknown"]

    print(f"Found {len(unnamed_devices)} unnamed devices to test...")
    print("Testing each device for Arduino characteristic...")
    print("-" * 70)

    arduino_found = False

    for i, device in enumerate(unnamed_devices, 1):
        print(f"\n[{i}/{len(unnamed_devices)}] Testing {device.address}...", end=" ", flush=True)

        is_arduino = await test_device(device)

        if is_arduino:
            print("✅ THIS IS YOUR ARDUINO!")
            print("\n" + "="*70)
            print("🎯 FOUND IT!")
            print("="*70)
            print(f"Arduino Address: {device.address}")
            print(f"Device Name: {device.name if device.name else 'Unnamed'}")
            print("\nYou can now use this address in your scripts!")
            print("="*70 + "\n")
            arduino_found = True
            return device.address
        else:
            print("❌ Not Arduino")

        # Small delay to avoid overwhelming Bluetooth
        await asyncio.sleep(0.3)

    if not arduino_found:
        print("\n" + "="*70)
        print("❌ Arduino not found in unnamed devices")
        print("="*70)
        print("\nPossible reasons:")
        print("1. Arduino is not powered on")
        print("2. Arduino is not running BLE code")
        print("3. Arduino is using a different characteristic UUID")
        print("4. Arduino is in the named devices list")
        print("\nTry:")
        print("- Check if Arduino is powered on and running")
        print("- Upload the BLE sketch to your Arduino")
        print("- Reset your Arduino and try again")
        print("="*70 + "\n")
        return None

if __name__ == "__main__":
    asyncio.run(find_arduino())
