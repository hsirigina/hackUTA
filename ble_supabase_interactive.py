#!/usr/bin/env python3
"""
Interactive version of ble_supabase.py - lets you choose which device to connect to
"""
import asyncio
import time
from datetime import datetime
from bleak import BleakClient, BleakScanner
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import the SupabaseDrivingMonitor class
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ble_supabase import SupabaseDrivingMonitor

async def main():
    # Get Arduino ID from user or use default
    arduino_id = input("Enter Arduino ID (default: ARD-001): ").strip() or "ARD-001"

    monitor = SupabaseDrivingMonitor(arduino_id=arduino_id)

    # Initialize session
    if not await monitor.initialize_session():
        return

    print("\n🔍 Scanning for Bluetooth devices...")
    print("=" * 60)

    # Scan for devices
    devices = await BleakScanner.discover(timeout=10.0)

    # Categorize devices
    named_devices = [d for d in devices if d.name and d.name != "Unknown"]
    unnamed_devices = [d for d in devices if not d.name or d.name == "Unknown"]

    print(f"\nFound {len(devices)} Bluetooth devices:\n")

    all_devices = []

    if named_devices:
        print("📱 NAMED DEVICES:")
        print("-" * 60)
        for i, device in enumerate(named_devices):
            idx = len(all_devices) + 1
            all_devices.append(device)
            print(f"{idx}. {device.name} ({device.address})")
        print()

    if unnamed_devices:
        print("❓ UNNAMED DEVICES (your Arduino might be here):")
        print("-" * 60)
        for i, device in enumerate(unnamed_devices):
            idx = len(all_devices) + 1
            all_devices.append(device)
            print(f"{idx}. Unnamed ({device.address})")
        print()

    print("=" * 60)

    # Let user choose
    while True:
        choice = input(f"\nEnter device number to connect (1-{len(all_devices)}) or 'q' to quit: ").strip()

        if choice.lower() == 'q':
            await monitor.end_session()
            return

        try:
            device_idx = int(choice) - 1
            if 0 <= device_idx < len(all_devices):
                selected_device = all_devices[device_idx]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(all_devices)}")
        except ValueError:
            print("❌ Invalid input. Please enter a number or 'q'")

    device_name = selected_device.name if selected_device.name else "Unnamed"
    print(f"\n✅ Connecting to: {device_name} ({selected_device.address})")

    try:
        async with BleakClient(selected_device.address, timeout=10.0) as client:
            print("✅ Connected!")

            # Show available services
            services = client.services
            print(f"\n📡 Device has {len(services.services)} services:")
            for service in services:
                print(f"   - {service.uuid}")

            # Try to find our characteristic
            target_char = "87654321-4321-4321-4321-cba987654321"
            char_found = False

            for service in services:
                for char in service.characteristics:
                    if str(char.uuid).lower() == target_char.lower():
                        char_found = True
                        print(f"\n🎯 Found driving monitor characteristic!")
                        break

            if not char_found:
                print(f"\n⚠️  WARNING: Characteristic {target_char} not found!")
                print("This device might not be your Arduino, or it's using a different UUID.")
                proceed = input("Continue anyway? (y/n): ").strip().lower()
                if proceed != 'y':
                    await monitor.end_session()
                    return

            print("\n📱 Starting to receive data...")
            print("Press Ctrl+C to disconnect")
            print("-" * 50)

            def notification_handler(sender, data):
                message = data.decode('utf-8')
                asyncio.create_task(monitor.process_data(message))

            # Try to start notifications
            try:
                await client.start_notify(target_char, notification_handler)
            except Exception as e:
                print(f"❌ Could not start notifications: {e}")
                print("This device might not support the expected characteristic.")
                await monitor.end_session()
                return

            # Keep connection alive
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n📊 Summary:")
                print(f"Total aggressive events: {monitor.event_count}")
                if monitor.aggressive_events:
                    print("Recent events:")
                    for event in monitor.aggressive_events[-5:]:
                        print(f"  - {event['time']}: {event['type']}")

                await monitor.end_session()
                print("Disconnected!")

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        await monitor.end_session()

if __name__ == "__main__":
    asyncio.run(main())
