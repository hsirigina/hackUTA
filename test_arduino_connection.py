#!/usr/bin/env python3
"""
Diagnostic script to test Arduino Bluetooth connection and Supabase integration
"""
import asyncio
import sys
from bleak import BleakScanner
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def test_supabase_connection():
    """Test if we can connect to Supabase"""
    print("\n" + "="*60)
    print("1. TESTING SUPABASE CONNECTION")
    print("="*60)

    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")

        if not url or not key:
            print("❌ FAILED: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env")
            return False

        print(f"✅ Found credentials")
        print(f"   URL: {url}")
        print(f"   Key: {key[:20]}...")

        supabase = create_client(url, key)

        # Test read
        result = supabase.table('drivers').select('*').eq('arduino_id', 'ARD-001').execute()
        if result.data:
            print(f"✅ Can READ from database")
            print(f"   Found driver: {result.data[0]['name']}")
        else:
            print("❌ FAILED: No driver found with ARD-001")
            return False

        # Test write
        update_result = supabase.table('drivers').update({
            'last_heartbeat': datetime.utcnow().isoformat()
        }).eq('arduino_id', 'ARD-001').execute()

        if update_result.data:
            print(f"✅ Can WRITE to database")
        else:
            print("❌ FAILED: Could not update driver")
            return False

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

async def test_bluetooth_scan():
    """Scan for Arduino Bluetooth device"""
    print("\n" + "="*60)
    print("2. SCANNING FOR ARDUINO BLUETOOTH")
    print("="*60)
    print("Looking for devices with 'Driving Monitor' or 'Arduino' in name...")
    print("Scanning for 10 seconds...")

    try:
        devices = await BleakScanner.discover(timeout=10.0)

        print(f"\n✅ Found {len(devices)} total Bluetooth devices")

        # Show all devices
        print("\nAll nearby devices:")
        for i, device in enumerate(devices, 1):
            name = device.name or "Unknown"
            print(f"  {i}. {name} ({device.address})")

        # Look for Arduino
        arduino_devices = []
        for device in devices:
            if device.name and ("Driving Monitor" in device.name or "Arduino" in device.name):
                arduino_devices.append(device)

        if arduino_devices:
            print(f"\n✅ Found {len(arduino_devices)} Arduino device(s):")
            for device in arduino_devices:
                print(f"   - {device.name} at {device.address}")
            return True
        else:
            print("\n❌ FAILED: No Arduino devices found")
            print("\nTroubleshooting:")
            print("  1. Make sure Arduino is powered on")
            print("  2. Check that BLE code is uploaded to Arduino")
            print("  3. Verify Arduino is advertising with name 'Driving Monitor'")
            print("  4. Try restarting the Arduino")
            return False

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

async def test_full_flow():
    """Test if ble_supabase.py can run (without actually connecting)"""
    print("\n" + "="*60)
    print("3. TESTING BLE_SUPABASE.PY IMPORTS")
    print("="*60)

    try:
        # Try importing the module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from ble_supabase import SupabaseDrivingMonitor

        print("✅ ble_supabase.py imports successfully")

        # Try creating an instance
        monitor = SupabaseDrivingMonitor(arduino_id="ARD-001")
        print("✅ SupabaseDrivingMonitor instance created")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

async def main():
    print("\n" + "="*60)
    print("ARDUINO → SUPABASE CONNECTION DIAGNOSTIC")
    print("="*60)

    # Run all tests
    supabase_ok = await test_supabase_connection()
    bluetooth_ok = await test_bluetooth_scan()
    flow_ok = await test_full_flow()

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Supabase Connection: {'✅ PASS' if supabase_ok else '❌ FAIL'}")
    print(f"Bluetooth Scanning:  {'✅ PASS' if bluetooth_ok else '❌ FAIL'}")
    print(f"Script Imports:      {'✅ PASS' if flow_ok else '❌ FAIL'}")

    if supabase_ok and bluetooth_ok and flow_ok:
        print("\n✅ All tests passed! You can now run:")
        print("   python3 ble_supabase.py")
    else:
        print("\n❌ Some tests failed. Fix the issues above before running ble_supabase.py")

    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
