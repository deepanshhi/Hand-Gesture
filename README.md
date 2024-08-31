# AI-Powered Virtual Mouse

This project is an AI-powered virtual mouse that allows users to control their computer's mouse and volume using hand gestures. The project utilizes Python's OpenCV for video capture, MediaPipe for hand tracking, and Pycaw for audio control. The hand gestures can perform various actions, such as moving the mouse, clicking, scrolling, and adjusting the volume.

## Features

- **Mouse Movement**: Control the mouse cursor by moving your hand in front of the camera.
- **Left Click Gesture**: Perform a left-click by bringing the thumb and index finger close together.
- **Right Click Gesture**: Perform a right-click by raising the index finger while the middle finger is lowered.
- **Volume Control**: Adjust the system volume based on the distance between the thumb and middle finger.
- **Volume Set Gesture**: Set the volume to a specific level by raising the index, middle, and thumb fingers.
- **Scrolling**: Scroll up or down by moving the hand to the top or bottom part of the camera view.

## Installation

To run this project, you need the following Python libraries:

- `opencv-python`
- `mediapipe`
- `pyautogui`
- `comtypes`
- `pycaw`

## Setup and Execution

1. **Clone the Repository**: Clone the repository to your local machine.
2. **Install Dependencies**: Install the required Python libraries using pip.
3. Run the Script: Execute the Python script in PyCharm or any other IDE.
     `python ai_virtual_mouse.py`
4. Camera Access: Ensure that your webcam is functional and accessible by the script.
5. Use Hand Gestures: Use the following gestures to control the mouse and volume:
      - *Move Mouse*: Move your hand to control the cursor.
      - *Left Click*: Bring the thumb and index finger together.
      - *Right Click*: Raise the index finger while the middle finger is lowered.
      - *Adjust Volume*: Change the volume by varying the distance between the thumb and middle finger.
      - *Set Specific Volume*: Raise the thumb, index, and middle fingers to set a specific volume level.
      - *Scroll*: Move the hand to the top or bottom of the camera view to scroll up or down.

## Customization

- **Volume Range**: Adjust the `SPECIFIC_VOLUME_LEVEL` variable in the script to set your desired specific volume level in decibels (dB).
- **Mouse Sensitivity**: Modify the `CAM_WIDTH`, `CAM_HEIGHT`, `SCREEN_WIDTH`, and `SCREEN_HEIGHT` constants to change the mouse sensitivity.
- **Gesture Thresholds**: Change the threshold values in the gesture detection functions to fine-tune the responsiveness of the gestures.

## Known Issues
- **Lighting Conditions**: Performance may vary under different lighting conditions. Ensure proper lighting for optimal hand detection.
- **Camera Quality**: A high-quality webcam is recommended for better hand tracking accuracy.

