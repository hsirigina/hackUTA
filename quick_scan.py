#!/usr/bin/env python3
"""
Quick Bluetooth scanner - just list all devices
"""
import asyncio
from bleak import BleakScanner

async def quick_scan():
    print("\n🔍 Scanning for Bluetooth devices (10 seconds)...\n")

    devices = await BleakScanner.discover(timeout=10.0)

    print(f"Found {len(devices)} devices:\n")
    print("-" * 70)

    for i, device in enumerate(devices, 1):
        name = device.name if device.name else "❓ Unnamed"
        print(f"{i:3d}. {name:30s} | {device.address}")

    print("-" * 70)
    print("\nLook for:")
    print("  - Any device with 'Arduino', 'Nano', 'BLE' in the name")
    print("  - Any unnamed device that might be your Arduino")
    print("\nTo test a specific device, note its address and we'll update the code.\n")

if __name__ == "__main__":
    asyncio.run(quick_scan())
