#!/usr/bin/env python3
"""
Camera Test Script
Tests iPhone Continuity Camera connection
"""
import cv2
import sys

print("\n" + "="*60)
print("📷 CAMERA CONNECTION TEST")
print("="*60)
print("\nTesting all available cameras...\n")

available_cameras = []

for i in range(10):  # Test indices 0-9
    print(f"Testing camera index {i}...", end=" ")
    cap = cv2.VideoCapture(i)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            height, width = frame.shape[:2]
            print(f"✅ WORKING! (Resolution: {width}x{height})")
            available_cameras.append({
                'index': i,
                'width': width,
                'height': height
            })
        else:
            print(f"⚠️  Opened but cannot read frames")
        cap.release()
    else:
        print("❌ Not available")

print("\n" + "="*60)
if available_cameras:
    print(f"✅ Found {len(available_cameras)} working camera(s):")
    for cam in available_cameras:
        print(f"   • Camera {cam['index']}: {cam['width']}x{cam['height']}")

    print("\n💡 Use camera index {} in your script".format(available_cameras[0]['index']))

    # Test the first available camera with live preview
    print("\n" + "="*60)
    print("Testing live video from camera {}...".format(available_cameras[0]['index']))
    print("Press 'q' to quit the preview")
    print("="*60 + "\n")

    cap = cv2.VideoCapture(available_cameras[0]['index'])

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break

        frame_count += 1

        # Add text overlay
        cv2.putText(frame, f"Camera {available_cameras[0]['index']} - Frame {frame_count}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Camera Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Camera test completed successfully!")

else:
    print("❌ NO CAMERAS FOUND!")
    print("\n📱 iPhone Continuity Camera Setup:")
    print("="*60)
    print("1. Make sure iPhone and Mac are on the same Apple ID")
    print("2. Enable Bluetooth and Wi-Fi on both devices")
    print("3. On Mac: System Settings > General > AirDrop & Handoff")
    print("   → Enable 'iPhone Continuity Camera'")
    print("4. On iPhone: Settings > General > AirPlay & Handoff")
    print("   → Enable 'Continuity Camera'")
    print("5. Wake your iPhone (don't unlock)")
    print("6. Try starting a FaceTime call first to activate the camera")
    print("7. Then run this test again")
    print("="*60)
    sys.exit(1)

print()
