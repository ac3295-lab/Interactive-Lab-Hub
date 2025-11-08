import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'

import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

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
dog1_path = "cute_ghost_dog.png"
dog2_path = "cute_ghost_dog_2.png"

dog1 = cv2.imread(dog1_path, cv2.IMREAD_UNCHANGED)
dog2 = cv2.imread(dog2_path, cv2.IMREAD_UNCHANGED)

if dog1 is None:
    raise FileNotFoundError(f"Could not load {dog1_path}")
if dog2 is None:
    raise FileNotFoundError(f"Could not load {dog2_path}")

dog1 = cv2.resize(dog1, (200, 200))
dog2 = cv2.resize(dog2, (150, 150))

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
minDist, maxDist = 50, 300
dog_alpha = 0.0
locked_alpha = None
photo_timer = None
photo_taken = False

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

    # ----------------------------------------
    # Hand detection and alpha control
    # ----------------------------------------
    if len(lmList) != 0:
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        pointerX, pointerY = lmList[8][1], lmList[8][2]
        cx, cy = (thumbX + pointerX) // 2, (thumbY + pointerY) // 2

        cv2.circle(img, (thumbX, thumbY), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pointerX, pointerY), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (pointerX, pointerY), (255, 0, 255), 2)

        if photo_timer is None:  # only adjust before countdown starts
            length = math.hypot(pointerX - thumbX, pointerY - thumbY)
            dog_alpha = np.interp(length, [minDist, maxDist], [0.0, 1.0])

            # Start countdown if dogs fully visible
            if dog_alpha > 0.8:
                photo_timer = time.time()
                locked_alpha = dog_alpha
                photo_taken = False
    else:
        if photo_timer is None and not photo_taken:
            cv2.putText(img, "Place your hand in view", (60, 200),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, "Pinch and widen your fingers for a surprise!", (20, 250),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

    # ----------------------------------------
    # Lock alpha once countdown starts
    # ----------------------------------------
    if photo_timer is not None:
        dog_alpha = locked_alpha if locked_alpha is not None else dog_alpha

    # ----------------------------------------
    # Overlay dogs on the image
    # ----------------------------------------
    img = overlay_image_alpha(img, dog1, (400, 150), alpha=dog_alpha)
    img = overlay_image_alpha(img, dog2, (100, 200), alpha=dog_alpha)

    # ----------------------------------------
    # Countdown and photo logic (runs regardless of hand visibility)
    # ----------------------------------------
    if photo_timer is not None and not photo_taken:
        elapsed = time.time() - photo_timer
        remaining = int(5 - elapsed)
        if remaining > 0:
            cv2.putText(img, f"Photo in {remaining}s", (200, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 0), 3)
        else:
            filename = f"ghost_dog_photo_{int(time.time())}.jpg"
            cv2.imwrite(filename, img)  # saves full frame WITH dogs + text
            cv2.putText(img, "Picture Taken!", (180, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 0), 3)
            print(f"Saved {filename}")
            photo_taken = True
            photo_timer = None

    # ----------------------------------------
    # FPS display
    # ----------------------------------------
    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    # ----------------------------------------
    # Show frame
    # ----------------------------------------
    cv2.imshow("Ghost Dog Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
