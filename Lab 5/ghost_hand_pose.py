import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

# -----------------------------
# CONFIG
# -----------------------------
dog_img_path = "cute_ghost_dog.png" 
wCam, hCam = 640, 480
minDist, maxDist = 50, 300  # Finger distance range
# -----------------------------

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

# Load the dog image with transparency (RGBA)
dog_img = cv2.imread(dog_img_path, cv2.IMREAD_UNCHANGED)
dog_img = cv2.resize(dog_img, (200, 200))

pTime = 0

def overlay_image_alpha(img, overlay, pos, alpha):
    """Overlay `overlay` onto `img` at `pos` with given alpha transparency."""
    x, y = pos
    h, w = overlay.shape[0], overlay.shape[1]

    if y + h > img.shape[0] or x + w > img.shape[1]:
        return img

    # Split out alpha channel
    if overlay.shape[2] == 4:
        overlay_rgb = overlay[:, :, :3]
        mask = overlay[:, :, 3:] / 255.0
    else:
        overlay_rgb = overlay
        mask = np.ones((h, w, 1), dtype=float)

    # Apply alpha factor
    mask = mask * alpha
    inv_mask = 1.0 - mask

    img[y:y+h, x:x+w] = (mask * overlay_rgb + inv_mask * img[y:y+h, x:x+w]).astype(np.uint8)
    return img


while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    alpha = 0.0  # transparency factor

    if len(lmList) != 0:
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        pointerX, pointerY = lmList[8][1], lmList[8][2]

        # Calculate distance
        length = math.hypot(pointerX - thumbX, pointerY - thumbY)

        # Map finger distance to opacity
        alpha = np.interp(length, [minDist, maxDist], [0.0, 1.0])
        alpha = np.clip(alpha, 0.0, 1.0)

        # Draw visuals
        cv2.circle(img, (thumbX, thumbY), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pointerX, pointerY), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (pointerX, pointerY), (255, 0, 255), 3)
        cv2.putText(img, f'Opacity: {alpha:.2f}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

    # Overlay dog image in top-left corner
    img = overlay_image_alpha(img, dog_img, (50, 150), alpha)

    # FPS counter
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Dog Opacity Control 🐶", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
