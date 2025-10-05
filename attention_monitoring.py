import cv2
import time
import numpy as np

print("\n=== ATTENTION MONITOR WITH EYE DETECTION ===")
print("Detecting faces and monitoring eye closure")
print("Press Ctrl+C to stop\n")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


counter = 0
frames_for_alert = 3
EAR_THRESHOLD = 0.25  # Threshold for eye closure detection
closed_eye_frames = 0

while True:
    try:
        ret, frame = cap.read()
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
        faces = face_cascade.detectMultiScale(gray, 1.05, 3)
        
        if len(faces) > 0:
            # Face detected, now check for eyes
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                
                # Detect eyes in the face region
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
                
                if len(eyes) >= 2:
                    # Both eyes detected - use simple area-based detection
                    eye_areas = []
                    for (ex, ey, ew, eh) in eyes:
                        eye_areas.append(ew * eh)
                    
                    # Sort by area and take the two largest (assuming they're the actual eyes)
                    eye_areas.sort(reverse=True)
                    
                    if len(eye_areas) >= 2:
                        avg_eye_area = (eye_areas[0] + eye_areas[1]) / 2
                        face_area = w * h
                        eye_to_face_ratio = avg_eye_area / face_area
                        
                        # Only detect closed eyes if eye area is extremely small
                        if eye_to_face_ratio < 0.0003:  # Very conservative threshold
                            closed_eye_frames += 1
                            print(f"😴 EYES CLOSED: Very small eye area detected ({closed_eye_frames}/{frames_for_alert})")
                        else:
                            print(f"👁️ PAYING ATTENTION: Eyes open and alert")
                            closed_eye_frames = 0
                            counter = 0
                    else:
                        print(f"👁️ PAYING ATTENTION: Eyes detected")
                        closed_eye_frames = 0
                        counter = 0
                elif len(eyes) == 1:
                    # Only one eye detected - might indicate closed eyes or poor detection
                    closed_eye_frames += 1
                    print(f"😴 POSSIBLE EYE CLOSURE: Only one eye detected ({closed_eye_frames}/{frames_for_alert})")
                else:
                    # No eyes detected in face - likely closed eyes
                    closed_eye_frames += 1
                    print(f"😴 EYES CLOSED: No eyes detected in face ({closed_eye_frames}/{frames_for_alert})")
                
                # Check if we should trigger alert
                if closed_eye_frames >= frames_for_alert:
                    print("\n🚨 ALERT: EYES CLOSED - NOT PAYING ATTENTION! 🚨\n")
                    closed_eye_frames = 0
                
                break  # Only process the first face found
        else:
            print(f"❌ NOT PAYING ATTENTION: No face detected ({counter + 1}/{frames_for_alert})")
            counter += 1
            closed_eye_frames = 0
            
            if counter >= frames_for_alert:
                print("\n🚨 ALERT: NOT PAYING ATTENTION! 🚨\n")
                counter = 0
        
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("\nStopping...")
        cap.release()
        break