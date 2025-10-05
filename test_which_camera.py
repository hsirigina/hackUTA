#!/usr/bin/env python3
"""
Test which camera shows your face - helps identify iPhone vs built-in camera
"""
import cv2
import sys

print("\n" + "="*60)
print("📷 CAMERA FACE DETECTION TEST")
print("="*60)
print("\nThis will help identify which camera can see your face best.\n")

cameras_to_test = [0, 1]  # Test both cameras

for cam_idx in cameras_to_test:
    print(f"\n{'='*60}")
    print(f"Testing Camera {cam_idx}")
    print(f"{'='*60}")

    cap = cv2.VideoCapture(cam_idx)

    if not cap.isOpened():
        print(f"❌ Camera {cam_idx} not available")
        continue

    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print(f"\n📹 Reading from camera {cam_idx}...")
    print("Position your face in front of the camera")
    print("Testing for 5 seconds...\n")

    import time
    start_time = time.time()
    face_detections = 0
    frames_tested = 0

    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break

        frames_tested += 1

        # Convert to grayscale and detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.05, 3)

        if len(faces) > 0:
            face_detections += 1
            print(f"✅ Face detected! ({face_detections}/{frames_tested} frames)")
        else:
            print(f"❌ No face ({face_detections}/{frames_tested} frames)")

        time.sleep(0.5)

    cap.release()

    detection_rate = (face_detections / frames_tested * 100) if frames_tested > 0 else 0

    print(f"\n📊 Results for Camera {cam_idx}:")
    print(f"   Frames tested: {frames_tested}")
    print(f"   Faces detected: {face_detections}")
    print(f"   Detection rate: {detection_rate:.1f}%")

    if detection_rate >= 50:
        print(f"   ✅ GOOD - This camera can see your face well!")
    elif detection_rate > 0:
        print(f"   ⚠️  PARTIAL - Face detected sometimes, try adjusting position")
    else:
        print(f"   ❌ POOR - No face detected, this might be the wrong camera")

print("\n" + "="*60)
print("RECOMMENDATION:")
print("="*60)

# Determine which camera is likely the iPhone
print("\n💡 Camera 0 is likely your Mac's built-in camera")
print("💡 Camera 1 is likely your iPhone Continuity Camera")
print("\nFor best results, use the camera with the highest detection rate.")
print("Position your iPhone to face you if using Camera 1.\n")
