import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize Mediapipe hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Variables to track the pinch state and movement direction
pinch_active = False
start_y = None

def detect_pinch(index_finger, thumb):
    distance = np.linalg.norm(np.array(index_finger) - np.array(thumb))
    return distance < 30  # Threshold distance to detect pinch

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a mirror-like view
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get the coordinates of the index finger tip and thumb tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert normalized coordinates to pixel values
            index_finger = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
            thumb = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect pinch
            if detect_pinch(index_finger, thumb):
                if not pinch_active:
                    pinch_active = True
                    start_y = index_finger[1]
                else:
                    end_y = index_finger[1]
                    if start_y is not None:
                        if end_y < start_y - 20:
                            print("Scroll Up")
                            pyautogui.scroll(10)  # Scroll up
                        elif end_y > start_y + 20:
                            print("Scroll Down")
                            pyautogui.scroll(-10)  # Scroll down
                        start_y = end_y
            else:
                pinch_active = False

    # Display the frame
    cv2.imshow('Finger Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
