#!/usr/bin/env python3
"""
Quick test to verify Supabase connection and data
"""
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    print("🧪 Testing Supabase Connection...\n")

    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url or not supabase_key:
        print("❌ Missing credentials in .env file")
        return False

    print(f"📡 Connecting to: {supabase_url}")

    try:
        # Create client
        supabase = create_client(supabase_url, supabase_key)
        print("✅ Connected to Supabase!\n")

        # Test: Get supervisors
        print("📋 Testing: Get supervisors...")
        supervisors = supabase.table('supervisors').select('*').execute()
        print(f"✅ Found {len(supervisors.data)} supervisor(s)")
        for sup in supervisors.data:
            print(f"   - {sup['name']} ({sup['email']})")

        # Test: Get drivers
        print("\n📋 Testing: Get drivers...")
        drivers = supabase.table('drivers').select('*').execute()
        print(f"✅ Found {len(drivers.data)} driver(s)")
        for driver in drivers.data:
            print(f"   - {driver['name']} | Arduino: {driver['arduino_id']} | Status: {driver['status']} | Score: {driver['safety_score']}")

        # Test: Get active sessions
        print("\n📋 Testing: Get active sessions...")
        sessions = supabase.table('driving_sessions').select('*').eq('status', 'active').execute()
        print(f"✅ Found {len(sessions.data)} active session(s)")

        # Test: Get events
        print("\n📋 Testing: Get events...")
        events = supabase.table('events').select('*').limit(5).execute()
        print(f"✅ Found {len(events.data)} recent event(s)")
        for event in events.data[:3]:
            print(f"   - {event['event_type']} | Severity: {event['severity']} | Arduino: {event['arduino_id']}")

        print("\n" + "="*50)
        print("✅ All tests passed! Ready to connect Arduino!")
        print("="*50)

        print("\n📝 Next steps:")
        print("1. Make sure your Arduino is powered on")
        print("2. Run: python ble_supabase.py")
        print("3. Default Arduino ID is ARD-001")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
