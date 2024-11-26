import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# PyCaw setup for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_volume, max_volume, _ = volume.GetVolumeRange()

# Function to calculate distance between two points
def calculate_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Start webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for a mirrored view
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Convert to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get landmark coordinates
                landmarks = hand_landmarks.landmark
                index_finger_tip = (int(landmarks[8].x * w), int(landmarks[8].y * h))
                thumb_tip = (int(landmarks[4].x * w), int(landmarks[4].y * h))

                # Draw circles on fingertips
                cv2.circle(frame, index_finger_tip, 10, (255, 0, 0), -1)
                cv2.circle(frame, thumb_tip, 10, (0, 255, 0), -1)

                # Draw a line between fingertips
                cv2.line(frame, index_finger_tip, thumb_tip, (255, 255, 0), 2)

                # Calculate distance and normalize volume
                distance = calculate_distance(index_finger_tip, thumb_tip)
                normalized_volume = np.interp(distance, [30, 150], [min_volume, max_volume])
                volume.SetMasterVolumeLevel(normalized_volume, None)

                # Display volume level on the frame
                volume_percent = np.interp(distance, [30, 150], [0, 100])
                cv2.putText(frame, f'Volume: {int(volume_percent)}%', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Gesture Volume Control', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
