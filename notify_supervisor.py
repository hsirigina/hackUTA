#!/usr/bin/env python3
"""
Supervisor Email Notification Service
Sends email to supervisor when a driver goes online
"""
import os
import sys
from dotenv import load_dotenv
from supabase import create_client
from email_notif import send_email_notification

load_dotenv()

def notify_supervisor_driver_online(driver_id: str):
    """Send email notification to all supervisors and default email when driver goes online"""
    try:
        # Initialize Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(supabase_url, supabase_key)

        # Get driver info
        driver = supabase.table('drivers').select('*').eq('id', driver_id).single().execute()

        if not driver.data:
            print(f"❌ Driver {driver_id} not found")
            return False

        driver_data = driver.data
        driver_name = driver_data['name']
        driver_email = driver_data.get('email', 'N/A')

        # Create email content
        subject = f"🚙 Driver Alert: {driver_name} is now ACTIVE"

        message = f"""Hello,

Driver {driver_name} ({driver_email}) has just started a driving session and is now ONLINE.

You can monitor their drive in real-time here:
http://localhost:5173/driver/{driver_id}

This is an automated notification from your Fleet Monitoring System.

---
Fleet Safety Monitoring System
"""

        # Collect all email recipients
        recipients = set()  # Use set to avoid duplicates

        # Add default notification email from .env
        default_email = os.getenv("NOTIFICATION_EMAIL") or os.getenv("DEFAULT_RECIPIENT")
        if default_email:
            recipients.add(default_email)

        # Get all supervisors from database
        supervisors = supabase.table('supervisors').select('email').execute()
        if supervisors.data:
            for supervisor in supervisors.data:
                if supervisor.get('email'):
                    recipients.add(supervisor['email'])

        if not recipients:
            print(f"⚠️ No recipients configured - skipping email notification")
            return False

        # Send email to all recipients
        emails_sent = 0
        for recipient in recipients:
            print(f"📧 Sending notification to {recipient}...")
            success = send_email_notification(subject, message, recipient)

            if success:
                print(f"   ✅ Email sent to {recipient}")
                emails_sent += 1
            else:
                print(f"   ❌ Failed to send to {recipient}")

        if emails_sent > 0:
            print(f"✅ Successfully sent {emails_sent} notification(s)")
            return True
        else:
            print(f"❌ No emails were sent")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        driver_id = sys.argv[1]
        notify_supervisor_driver_online(driver_id)
    else:
        print("Usage: python3 notify_supervisor.py <driver_id>")
