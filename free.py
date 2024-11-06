import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import time

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Function to check if two landmarks are close enough to be considered touching
def fingers_touching(landmark1, landmark2, threshold=0.03):
    distance = ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5
    return distance < threshold

# Open YouTube Shorts in the default web browser
webbrowser.open("https://www.youtube.com/shorts", new=2)
time.sleep(2)  # Give browser time to open

# Main loop
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            
            # Scroll up when thumb and index finger touch
            if fingers_touching(thumb_tip, index_tip):
                print("Scrolling up")  # Debugging message
                pyautogui.scroll(100)  # Increased scroll amount
            
            # Scroll down when thumb and middle finger touch
            elif fingers_touching(thumb_tip, middle_tip):
                print("Scrolling down")  # Debugging message
                pyautogui.scroll(-100)  # Increased scroll amount

    # Show image with hand landmarks
    cv2.imshow('Hand Tracking', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(5) & 0xFF == 27:  # Exit on pressing 'Esc'
        break

cap.release()
cv2.destroyAllWindows()
