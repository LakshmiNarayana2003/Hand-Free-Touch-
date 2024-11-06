# Gesture-Based Scrolling with Hand Tracking

This project implements a gesture-controlled scrolling application using OpenCV, MediaPipe, and PyAutoGUI. The program opens YouTube Shorts in a web browser and allows users to scroll up and down using hand gestures captured via webcam. Specifically, the application detects the following gestures:

- **Scroll Up**: Touch your thumb and index finger together.
- **Scroll Down**: Touch your thumb and middle finger together.

This hands-free interaction is achieved using real-time hand landmark detection and simple Python automation.

## Features

- **Gesture Recognition**: Detects specific finger gestures using MediaPipe’s hand tracking.
- **Automatic Scrolling**: Initiates scroll actions on detecting the appropriate gesture.
- **Real-Time Video Feed**: Displays the webcam feed with annotated hand landmarks for live feedback.

## Requirements

Make sure to install the following dependencies:

```bash
pip install opencv-python mediapipe pyautogui
