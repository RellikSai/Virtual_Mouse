#Imports
import time
import cv2
import numpy as np
import pyautogui
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#Importing Hand-Detection Files
MODEL_PATH = "hand_landmarker.task"

#Defining Variables and thresholds
SMOOTHING_ALPHA = 0.25
PINCH_THRESH = 0.035
SCROLL_PAIR_THRESH = 0.04
ZOOM_THRESH = 0.08
CLICK_DEBOUNCE_SECONDS = 0.35
CLICK_DEBOUNCE_SECOND = 0.50
DRAG_HOLD_SECONDS = 0.5
ACTIVE_MARGIN = 0.12
CAM_INDEX = 0

SHOW_HUD = True
pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

#Function to calculate distance
def norm_dist(a, b):
    return np.linalg.norm([a.x - b.x, a.y - b.y])

class EMA:
    def __init__(self, alpha):
        self.alpha = alpha
        self.value = None

    def update(self, new):
        new = np.array(new)
        self.value = new if self.value is None else (
            self.alpha * new + (1 - self.alpha) * self.value
        )
        return self.value

#Function to scale screen size and store in pyplotgui to control mouse accordingly 
def map_to_screen(nx, ny):
    m = ACTIVE_MARGIN
    nx = np.clip((nx - m) / (1 - 2 * m), 0, 1)
    ny = np.clip((ny - m) / (1 - 2 * m), 0, 1)
    return int(nx * screen_w), int(ny * screen_h)

#Function to capture video in a desired resolution
def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    base_options = python.BaseOptions(
        model_asset_path=MODEL_PATH
    )

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6
    )

    detector = vision.HandLandmarker.create_from_options(options)

    ema = EMA(SMOOTHING_ALPHA)

    last_click_time = 0
    pinch_start_time = None
    dragging = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = detector.detect(mp_image)

        if result.hand_landmarks:
            lm = result.hand_landmarks[0]

            #Defining each finger tips
            thumb = lm[4]
            index = lm[8]
            middle = lm[12]
            pinky = lm[20]

            #Distance between required finger tips
            d_ti = norm_dist(thumb, index)
            d_tm = norm_dist(thumb, middle)
            d_mp = norm_dist(middle, pinky)
            d_tp = norm_dist(thumb, pinky)

            sx, sy = map_to_screen(index.x, index.y)
            sx, sy = ema.update((sx, sy))
            pyautogui.moveTo(int(sx), int(sy), duration=0)

            current_time = time.time()

            if d_ti < PINCH_THRESH:
                if pinch_start_time is None:
                    pinch_start_time = current_time
                elif (current_time - pinch_start_time > DRAG_HOLD_SECONDS
                      and not dragging):
                    pyautogui.mouseDown()
                    dragging = True
                elif not dragging:
                    if current_time - last_click_time > CLICK_DEBOUNCE_SECONDS:
                        pyautogui.click()
                        last_click_time = current_time
            else:
                pinch_start_time = None
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            if d_tm < PINCH_THRESH:
                if current_time - last_click_time > CLICK_DEBOUNCE_SECONDS:
                    pyautogui.click(button="right")
                    last_click_time = current_time

            if d_tp < PINCH_THRESH:
                if current_time - last_click_time > CLICK_DEBOUNCE_SECOND:
                    pyautogui.hotkey('alt', 'f4')
                    last_click_time = current_time

            if d_mp < PINCH_THRESH:
                if d_ti < ZOOM_THRESH:
                    pyautogui.scroll(-120)
                elif d_ti > ZOOM_THRESH:
                    pyautogui.scroll(120)

            if SHOW_HUD:
                for p in lm:
                    cv2.circle(frame, (int(p.x * frame.shape[1]), int(p.y * frame.shape[0])), 3, (0, 255, 0), -1)

        cv2.imshow("Computer Vision: A Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF in (27, ord("q")):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

