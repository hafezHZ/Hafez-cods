import cv2
import mediapipe as mp
import numpy as np
import os
import time
import urllib.request

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- SETTINGS ----------------

MODEL_FILE = "hand_landmarker.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

WIDTH = 1280
HEIGHT = 720
BRUSH_SIZE = 8
ERASER_SIZE = 45

COLORS = {
    "1": ("BLUE", (255, 0, 0)),
    "2": ("GREEN", (0, 255, 0)),
    "3": ("RED", (0, 0, 255)),
    "4": ("YELLOW", (0, 255, 255)),
    "5": ("PURPLE", (255, 0, 255)),
    "6": ("WHITE", (255, 255, 255)),
}

# ---------------- DOWNLOAD MODEL ----------------

if not os.path.exists(MODEL_FILE):
    print("Downloading hand tracking model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_FILE)

# ---------------- MEDIAPIPE ----------------

BaseOptions = python.BaseOptions

options = vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_FILE),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)

# ---------------- CAMERA ----------------

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

if not camera.isOpened():
    raise RuntimeError("Camera could not be opened!")

canvas = None
previous_point = None
selected_color = (255, 0, 0)
eraser = False
last_timestamp = 0

# ---------------- FUNCTIONS ----------------

def finger_up(hand, tip, pip):
    return hand[tip].y < hand[pip].y


def draw_interface(frame):
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 75), (25, 25, 25), -1)

    cv2.putText(
        frame,
        "HAFEZ AIR PAINT PRO",
        (20, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "1-6 COLORS | E ERASER | C CLEAR | S SAVE | Q EXIT",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (200, 200, 200),
        1
    )

    x = 500
    for key, (name, color) in COLORS.items():
        cv2.circle(frame, (x, 35), 13, color, -1)
        cv2.putText(
            frame, key, (x - 5, 62),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4,
            (255, 255, 255), 1
        )
        x += 65

    status = "ERASER" if eraser else "DRAW"
    cv2.putText(
        frame, status,
        (frame.shape[1] - 130, 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


def save_image():
    filename = f"HAFEZ_PAINT_{int(time.time())}.png"
    cv2.imwrite(filename, canvas)
    print("Saved:", filename)


# ---------------- MAIN LOOP ----------------

try:
    while True:
        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        h, w = frame.shape[:2]

        if canvas is None:
            canvas = np.zeros((h, w, 3), dtype=np.uint8)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp = max(
            last_timestamp + 1,
            time.monotonic_ns() // 1_000_000
        )
        last_timestamp = timestamp

        result = detector.detect_for_video(mp_image, timestamp)

        current_point = None
        drawing = False

        if result.hand_landmarks:
            for hand in result.hand_landmarks:

                index_up = finger_up(hand, 8, 6)
                middle_up = finger_up(hand, 12, 10)

                index_x = int(hand[8].x * w)
                index_y = int(hand[8].y * h)

                middle_x = int(hand[12].x * w)
                middle_y = int(hand[12].y * h)

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    9,
                    (0, 255, 255),
                    -1
                )

                # Index only = drawing
                if index_up and not middle_up:
                    drawing = True
                    current_point = (index_x, index_y)

                # Index + middle = pause drawing
                elif index_up and middle_up:
                    previous_point = None

        if drawing and current_point is not None:
            if previous_point is not None:
                size = ERASER_SIZE if eraser else BRUSH_SIZE
                color = (0, 0, 0) if eraser else selected_color

                cv2.line(
                    canvas,
                    previous_point,
                    current_point,
                    color,
                    size,
                    cv2.LINE_AA
                )

            previous_point = current_point
        else:
            previous_point = None

        # Blend canvas and camera
        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        inverse = cv2.bitwise_not(mask)

        background = cv2.bitwise_and(frame, frame, mask=inverse)
        foreground = cv2.bitwise_and(canvas, canvas, mask=mask)

        output = cv2.add(background, foreground)

        draw_interface(output)

        cv2.imshow("HAFEZ AIR PAINT PRO", output)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("c"):
            canvas[:] = 0
            previous_point = None

        elif key == ord("e"):
            eraser = not eraser
            previous_point = None

        elif key == ord("s"):
            save_image()

        elif chr(key) in COLORS:
            selected_color = COLORS[chr(key)][1]
            eraser = False
            previous_point = None

finally:
    camera.release()
    detector.close()
    cv2.destroyAllWindows()