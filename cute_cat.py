import cv2
import mediapipe as mp
import time
import os

# Initialize MediaPipe Hand Tracking
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1)
mpDraw = mp.solutions.drawing_utils

# Capture Video
cap = cv2.VideoCapture(0)

# Gesture Definitions (Mapped to NirCmd Commands)
GESTURE_ACTIONS = {
    "thumbs_up": "volume_up",
    "thumbs_down": "volume_down",
    "fist": "mute_audio",
    "open_palm": "play_pause",
    "swipe_right": "next_track",
    "swipe_left": "previous_track"
}

def execute_command(command):
    """Executes system-level commands based on recognized gestures."""
    if command == "volume_up":
        os.system('nircmd.exe changesysvolume 15000')  # Increase volume
    elif command == "volume_down":
        os.system('nircmd.exe changesysvolume -15000')  # Decrease volume
    elif command == "mute_audio":
        os.system('nircmd.exe mutesysvolume 2')  # Toggle mute
    elif command == "play_pause":
        os.system('nircmd.exe sendkeypress space')  # Simulates spacebar (for Play/Pause)
    elif command == "next_track":
        os.system('nircmd.exe sendkeypress media_next')  # Next track
    elif command == "previous_track":
        os.system('nircmd.exe sendkeypress media_prev')  # Previous track
    else:
        print("Unknown command received:", command)

# Main Loop
while True:
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    detected_gesture = None

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Detect thumb up or fist gesture (for demo, detect closed fingers)
            finger_count = sum([1 for i in range(5) if handLms.landmark[i].y < handLms.landmark[i+4].y])

            if finger_count == 0:
                detected_gesture = "fist"
            elif finger_count == 5:
                detected_gesture = "open_palm"
            elif finger_count == 1 and handLms.landmark[4].y < handLms.landmark[3].y:
                detected_gesture = "thumbs_up"
            elif finger_count == 1 and handLms.landmark[4].y > handLms.landmark[3].y:
                detected_gesture = "thumbs_down"

    # If a gesture is detected, execute corresponding command
    if detected_gesture and detected_gesture in GESTURE_ACTIONS:
        print(f"Recognized Gesture: {detected_gesture}")  # Debugging output
        execute_command(GESTURE_ACTIONS[detected_gesture])

  
    # Show image
    cv2.imshow("Hand Gesture Control", img)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
