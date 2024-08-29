import cv2
import mediapipe as mp
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import hypot

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize Pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAM_WIDTH, CAM_HEIGHT = 640, 480
SPECIFIC_VOLUME_LEVEL = -20.0  # Set this to your desired volume level in dB

# Hand connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),   # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),   # Index finger
    (0, 9), (9, 10), (10, 11), (11, 12), # Middle finger
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky
]

def calculate_distance(point1, point2):
    return hypot(point2[0] - point1[0], point2[1] - point1[1])

def move_mouse(x, y):
    screen_x = SCREEN_WIDTH * (x / CAM_WIDTH)
    screen_y = SCREEN_HEIGHT * (y / CAM_HEIGHT)
    pyautogui.moveTo(screen_x, screen_y)

def control_volume(dist):
    vol = min_vol + (max_vol - min_vol) * (dist / 200)  # Adjust 200 as needed
    vol = max(min_vol, min(vol, max_vol))
    volume.SetMasterVolumeLevel(vol, None)

def set_volume_at_specific_level():
    volume.SetMasterVolumeLevel(SPECIFIC_VOLUME_LEVEL, None)

def detect_gesture(landmarks):
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    thumb_pip = landmarks[mp_hands.HandLandmark.THUMB_IP]

    index_tip_y = index_tip.y
    middle_tip_y = middle_tip.y
    thumb_tip_y = thumb_tip.y
    index_pip_y = index_pip.y
    middle_pip_y = middle_pip.y
    thumb_pip_y = thumb_pip.y

    # Detect Left Click Gesture: Thumb and index finger are close together
    thumb_index_dist = calculate_distance(
        (landmarks[mp_hands.HandLandmark.THUMB_TIP].x * CAM_WIDTH, landmarks[mp_hands.HandLandmark.THUMB_TIP].y * CAM_HEIGHT),
        (index_tip.x * CAM_WIDTH, index_tip.y * CAM_HEIGHT)
    )
    if thumb_index_dist < 30:  # threshold
        pyautogui.click(button='left')
        print("left click")

    # Detect Right Click Gesture: Index finger is raised, middle finger is lowered
    if index_tip_y < index_pip_y and middle_tip_y > middle_pip_y:
        pyautogui.click(button='right')
        print("right click")

    # Detect Volume Set Gesture: Index, middle, and thumb fingers are all up
    if (index_tip_y < index_pip_y) and (middle_tip_y < middle_pip_y) and (thumb_tip_y < thumb_pip_y):
        set_volume_at_specific_level()
        return True

    return False

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

volume_frozen = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Draw the rectangular boundary box
    cv2.rectangle(frame, (10, 10), (CAM_WIDTH - 10, CAM_HEIGHT - 10), (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            thumb_x, thumb_y = int(thumb_tip.x * CAM_WIDTH), int(thumb_tip.y * CAM_HEIGHT)
            index_x, index_y = int(index_tip.x * CAM_WIDTH), int(index_tip.y * CAM_HEIGHT)
            middle_x, middle_y = int(middle_tip.x * CAM_WIDTH), int(middle_tip.y * CAM_HEIGHT)

            # Calculate the average position of index and middle fingers
            avg_x = (index_x + middle_x) // 2
            avg_y = (index_y + middle_y) // 2

            # Move mouse based on average position of index and middle fingers
            move_mouse(avg_x, avg_y)

            # Detect gesture for clicking and setting volume
            frozen = detect_gesture(landmarks)
            if not frozen:
                # Control volume based on distance between thumb and middle finger
                thumb_middle_dist = calculate_distance((thumb_x, thumb_y), (middle_x, middle_y))
                control_volume(thumb_middle_dist)

            # Scroll based on the position of both index and middle fingers
            if index_y < CAM_HEIGHT // 3 and middle_y < CAM_HEIGHT // 3:
                pyautogui.scroll(50)  # Scroll up, increased speed
                print("scroll up")
            elif index_y > 2 * CAM_HEIGHT // 3 and middle_y > 2 * CAM_HEIGHT // 3:
                pyautogui.scroll(-40)  # Scroll down, increased speed
                print("scroll down")
            else:
                print(f"outside {index_y} {middle_y}")

            # Draw the hand landmarks
            for connection in HAND_CONNECTIONS:
                start_idx, end_idx = connection
                start = landmarks[start_idx]
                end = landmarks[end_idx]
                start_point = (int(start.x * CAM_WIDTH), int(start.y * CAM_HEIGHT))
                end_point = (int(end.x * CAM_WIDTH), int(end.y * CAM_HEIGHT))
                cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

            # Draw landmarks
            for landmark in landmarks:
                x = int(landmark.x * CAM_WIDTH)
                y = int(landmark.y * CAM_HEIGHT)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    cv2.imshow('AI Virtual Mouse', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
