import os
# Force Qt to use X11 instead of Wayland (important on Raspberry Pi)
os.environ['QT_QPA_PLATFORM'] = 'xcb'

import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import subprocess

# -----------------------------
# Video setup
# -----------------------------
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.handDetector(detectionCon=1)

# -----------------------------
# Dog overlay setup
# -----------------------------
dog_img_path = "cute_ghost_dog.png"
dog_img = cv2.imread(dog_img_path, cv2.IMREAD_UNCHANGED)
if dog_img is None:
    raise FileNotFoundError(f"Could not load {dog_img_path}")
dog_img = cv2.resize(dog_img, (200, 200))

def overlay_image_alpha(background, overlay, pos, alpha=1.0):
    """Overlay RGBA image `overlay` onto `background` at position `pos`."""
    x, y = pos
    h, w = overlay.shape[:2]
    if y + h > background.shape[0] or x + w > background.shape[1]:
        return background

    overlay_img = overlay[:, :, :3]
    mask = overlay[:, :, 3:] / 255.0
    mask = mask * alpha
    inv_mask = 1 - mask

    background[y:y+h, x:x+w] = (
        mask * overlay_img + inv_mask * background[y:y+h, x:x+w]
    ).astype(np.uint8)
    return background

# -----------------------------
# Control parameters
# -----------------------------
minVol, maxVol = 0, 100
minDist, maxDist = 50, 300
volBar, volPer = 400, 0
dog_alpha = 0.0  # transparency for dog overlay

# -----------------------------
# Main loop
# -----------------------------
while True:
    success, img = cap.read()
    if not success:
        print("Camera read failed.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        pointerX, pointerY = lmList[8][1], lmList[8][2]
        cx, cy = (thumbX + pointerX) // 2, (thumbY + pointerY) // 2

        cv2.circle(img, (thumbX, thumbY), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pointerX, pointerY), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (pointerX, pointerY), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Distance between thumb and index
        length = math.hypot(pointerX - thumbX, pointerY - thumbY)

        # Map distance to volume and alpha
        vol = np.interp(length, [minDist, maxDist], [minVol, maxVol])
        volBar = np.interp(length, [minDist, maxDist], [400, 150])
        volPer = np.interp(length, [minDist, maxDist], [0, 100])
        dog_alpha = np.interp(length, [minDist, maxDist], [0.0, 1.0])

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Volume bar and FPS
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Overlay the ghost dog
    img = overlay_image_alpha(img, dog_img, (400, 150), alpha=dog_alpha)

    cv2.imshow("Ghost Dog Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        audio_process.terminate()
        break

cap.release()
cv2.destroyAllWindows()
