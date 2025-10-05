#!/usr/bin/env python3
"""
Enhanced Bluetooth scanner to find Arduino by trying to connect to unknown devices
"""
import asyncio
from bleak import BleakScanner, BleakClient

async def scan_and_inspect():
    print("\n" + "="*60)
    print("ENHANCED BLUETOOTH SCANNER - Finding Your Arduino")
    print("="*60)
    print("\nScanning for 15 seconds...")

    devices = await BleakScanner.discover(timeout=15.0)

    print(f"\n✅ Found {len(devices)} total Bluetooth devices\n")

    # Categorize devices
    named_devices = []
    unnamed_devices = []

    for device in devices:
        if device.name and device.name != "Unknown":
            named_devices.append(device)
        else:
            unnamed_devices.append(device)

    # Show named devices
    if named_devices:
        print(f"📱 NAMED DEVICES ({len(named_devices)}):")
        print("-" * 60)
        for i, device in enumerate(named_devices, 1):
            print(f"{i}. {device.name}")
            print(f"   Address: {device.address}")
            print()

    # Show unnamed devices
    print(f"\n❓ UNNAMED DEVICES ({len(unnamed_devices)}):")
    print("-" * 60)
    print("These could be your Arduino if it's not setting a device name.\n")

    for i, device in enumerate(unnamed_devices, 1):
        print(f"{i}. Address: {device.address}")

        # Try to get more details by attempting connection
        try:
            async with BleakClient(device.address, timeout=2.0) as client:
                if client.is_connected:
                    print(f"   ✅ CONNECTABLE!")

                    # Try to get services
                    services = client.services
                    if services:
                        print(f"   Services found: {len(services.services)}")
                        for service in services:
                            print(f"      - {service.uuid}")
                            # Check if it has our characteristic
                            if "87654321-4321-4321-4321-cba987654321" in [str(char.uuid) for char in service.characteristics]:
                                print(f"      ⭐ FOUND DRIVING MONITOR CHARACTERISTIC!")
                                print(f"      🎯 THIS IS LIKELY YOUR ARDUINO!")
        except Exception as e:
            print(f"   ❌ Cannot connect: {str(e)[:50]}")

        print()

        # Rate limit to avoid overwhelming Bluetooth
        await asyncio.sleep(0.5)

    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("1. Look for devices marked with ⭐ or ✅ CONNECTABLE")
    print("2. If you found your Arduino, note its address")
    print("3. You can manually connect using the address in ble_supabase.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(scan_and_inspect())
