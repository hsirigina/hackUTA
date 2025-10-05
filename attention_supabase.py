#!/usr/bin/env python3
"""
Attention Monitoring with Supabase Integration
Monitors driver attention using facial recognition and saves events to Supabase
"""
import cv2
import time
import asyncio
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import sys

# Force unbuffered output so logs show in real-time
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Load environment variables
load_dotenv()

class AttentionMonitor:
    def __init__(self, driver_arduino_id: str = "642B8DC2-D778-8A47-20C2-B91C64716DBF", iphone_camera_index: int = None):
        self.driver_arduino_id = driver_arduino_id
        self.driver_id = None
        self.session_id = None

        # Attention tracking
        self.counter = 0
        self.frames_for_alert = 3
        self.closed_eye_frames = 0
        self.last_attention_score_update = time.time()

        # Event cooldown to prevent duplicates (similar to Arduino)
        self.last_event_timestamps = {
            'DISTRACTED': 0,
            'DROWSY': 0,
            'EYES_CLOSED': 0
        }
        self.EVENT_COOLDOWN_SECONDS = 5.0  # 5 seconds between same event type

        # Initialize Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file")

        self.supabase: Client = create_client(supabase_url, supabase_key)
        print(f"✅ Connected to Supabase")

        # Initialize CV2 - Use iPhone camera (index 1)
        IPHONE_CAMERA_INDEX = iphone_camera_index if iphone_camera_index is not None else 1

        print(f"\n📱 Connecting to iPhone camera (index {IPHONE_CAMERA_INDEX})...")

        self.cap = cv2.VideoCapture(IPHONE_CAMERA_INDEX)

        if self.cap.isOpened():
            ret, test_frame = self.cap.read()
            if ret and test_frame is not None:
                print(f"✅ iPhone camera connected!")
                print(f"   Resolution: {test_frame.shape[1]}x{test_frame.shape[0]}")
                camera_found = True
            else:
                print("❌ Cannot read from iPhone camera!")
                self.cap.release()
                camera_found = False
        else:
            camera_found = False

        if not camera_found:
            print("\n⚠️  No camera available!")
            print("📱 The attention monitoring will not run.")
            print("   To use attention monitoring:")
            print("   1. Connect your iPhone via Continuity Camera")
            print("   2. Or ensure your Mac's built-in camera is available")
            print("   3. Then restart the monitoring system")
            raise ValueError("No camera available - attention monitoring disabled")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        print(f"✅ Face/eye detection models loaded")

    def find_active_session(self):
        """Find the active driving session for this driver"""
        try:
            # Find driver by Arduino ID
            driver_response = self.supabase.table('drivers').select('*').eq('arduino_id', self.driver_arduino_id).execute()

            if not driver_response.data:
                print(f"❌ Driver not found for Arduino ID: {self.driver_arduino_id}")
                return False

            driver = driver_response.data[0]
            self.driver_id = driver['id']
            print(f"✅ Found driver: {driver['name']} ({driver['email']})")

            # Find MOST RECENT active session for this driver (same one BLE is using)
            session_response = self.supabase.table('driving_sessions').select('*').eq('driver_id', self.driver_id).eq('status', 'active').order('started_at', desc=True).limit(1).execute()

            if not session_response.data:
                print(f"⚠️  No active driving session found - waiting for session to start...")
                return False

            self.session_id = session_response.data[0]['id']
            print(f"✅ Found active session: {self.session_id}")
            print(f"   Session started at: {session_response.data[0]['started_at'][:19]}")
            return True

        except Exception as e:
            print(f"❌ Error finding session: {e}")
            return False

    def save_attention_event(self, event_type: str, description: str):
        """Save attention event to Supabase"""
        try:
            # Check cooldown
            current_time = time.time()
            time_since_last = current_time - self.last_event_timestamps.get(event_type, 0)

            if time_since_last < self.EVENT_COOLDOWN_SECONDS:
                return  # Skip duplicate event

            # Update last event timestamp
            self.last_event_timestamps[event_type] = current_time

            if not self.session_id:
                # Try to find active session
                if not self.find_active_session():
                    return

            # Save event
            event_data = {
                'session_id': self.session_id,
                'driver_id': self.driver_id,
                'arduino_id': self.driver_arduino_id,
                'event_type': event_type,
                'x': 0,  # Not applicable for attention events
                'y': 0,
                'z': 0,
                'count_at_time': 0,
                'severity': 'high' if event_type in ['DROWSY', 'EYES_CLOSED'] else 'medium',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

            self.supabase.table('events').insert(event_data).execute()

            # Calculate penalty (doubled for faster demo)
            penalty_points = {
                'DISTRACTED': 6,    # Looking away
                'DROWSY': 10,        # Eyes closed
                'EYES_CLOSED': 10    # No eyes detected
            }.get(event_type, 6)

            print(f"💾 {event_type} event | Safety score -{penalty_points}")

            # Update safety score
            self.update_safety_score(penalty_points)

        except Exception as e:
            print(f"⚠️  Error saving event: {e}")

    def update_safety_score(self, penalty_points: int):
        """Update safety score by applying penalty"""
        try:
            if not self.session_id:
                return

            # Get current session score
            session = self.supabase.table('driving_sessions').select('*').eq('id', self.session_id).execute()

            if session.data:
                current_score = session.data[0].get('safety_score', 100)
                new_score = max(0, current_score - penalty_points)

                # Update session
                self.supabase.table('driving_sessions').update({
                    'safety_score': new_score
                }).eq('id', self.session_id).execute()

                # Update driver
                self.supabase.table('drivers').update({
                    'safety_score': new_score,
                    'last_active': datetime.now(timezone.utc).isoformat()
                }).eq('id', self.driver_id).execute()

                print(f"📊 Safety score updated: {current_score} → {new_score}")

        except Exception as e:
            print(f"⚠️  Error updating score: {e}")

    def process_frame(self, frame, gray, faces):
        """Process frame for attention detection"""
        # Debug: Print every 10th frame to show it's running
        if not hasattr(self, '_frame_count'):
            self._frame_count = 0
        self._frame_count += 1

        if len(faces) > 0:
            # Face detected, now check for eyes
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                # More lenient eye detection: minNeighbors 3 (was 5)
                eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3, minSize=(15, 15))

                if len(eyes) >= 2:
                    # Both eyes detected
                    eye_areas = [ew * eh for (ex, ey, ew, eh) in eyes]
                    eye_areas.sort(reverse=True)

                    if len(eye_areas) >= 2:
                        avg_eye_area = (eye_areas[0] + eye_areas[1]) / 2
                        face_area = w * h
                        eye_to_face_ratio = avg_eye_area / face_area

                        if eye_to_face_ratio < 0.0003:
                            self.closed_eye_frames += 1
                            print(f"😴 EYES CLOSED: Very small eye area ({self.closed_eye_frames}/{self.frames_for_alert})")

                            if self.closed_eye_frames >= self.frames_for_alert:
                                print("🚨 ALERT: DROWSY - EYES CLOSED!")
                                self.save_attention_event('DROWSY', 'Eyes closed - driver drowsy')
                                self.closed_eye_frames = 0
                        else:
                            print(f"👁️ PAYING ATTENTION")
                            self.closed_eye_frames = 0
                            self.counter = 0
                    else:
                        print(f"👁️ PAYING ATTENTION")
                        self.closed_eye_frames = 0
                        self.counter = 0

                elif len(eyes) == 1:
                    self.closed_eye_frames += 1
                    print(f"😴 POSSIBLE EYE CLOSURE: One eye ({self.closed_eye_frames}/{self.frames_for_alert})")

                    if self.closed_eye_frames >= self.frames_for_alert:
                        print("🚨 ALERT: EYES CLOSED!")
                        self.save_attention_event('EYES_CLOSED', 'Only one eye detected')
                        self.closed_eye_frames = 0
                else:
                    # No eyes detected
                    self.closed_eye_frames += 1
                    print(f"😴 EYES CLOSED: No eyes detected ({self.closed_eye_frames}/{self.frames_for_alert})")

                    if self.closed_eye_frames >= self.frames_for_alert:
                        print("🚨 ALERT: EYES CLOSED!")
                        self.save_attention_event('EYES_CLOSED', 'No eyes detected in face')
                        self.closed_eye_frames = 0

                break  # Process first face only
        else:
            # No face detected - driver looking away
            print(f"❌ NOT PAYING ATTENTION: No face detected ({self.counter + 1}/{self.frames_for_alert})")
            self.counter += 1
            self.closed_eye_frames = 0

            if self.counter >= self.frames_for_alert:
                print("🚨 ALERT: DISTRACTED - NOT LOOKING AT ROAD!")
                self.save_attention_event('DISTRACTED', 'No face detected - looking away')
                self.counter = 0

    def run(self):
        """Main monitoring loop"""
        print("\n=== ATTENTION MONITOR WITH SUPABASE ===", flush=True)
        print("Monitoring driver attention and saving to Supabase", flush=True)
        print("Press Ctrl+C to stop\n", flush=True)

        # Wait for active session
        while not self.find_active_session():
            print("⏳ Waiting for active driving session...", flush=True)
            time.sleep(3)

        print("\n🟢 Session found - starting attention monitoring!\n", flush=True)

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    continue

                # Resize frame
                height, width = frame.shape[:2]
                if width > 800:
                    scale = 800 / width
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    frame = cv2.resize(frame, (new_width, new_height))

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # More lenient face detection for iPhone camera
                # scaleFactor: 1.1 (was 1.05, higher = faster but less accurate)
                # minNeighbors: 2 (was 3, lower = more detections)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 2, minSize=(30, 30))

                self.process_frame(frame, gray, faces)

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\n🛑 Stopping attention monitoring...")
            self.cap.release()
            print("✅ Camera released")

def main():
    monitor = AttentionMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
