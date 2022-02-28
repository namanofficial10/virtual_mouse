import cv2
import mediapipe as mp
import time
import hand_track_module as htm
import math
import pyautogui
import numpy as np
from datetime import datetime

try:
    class DragRect():
        def __init__(self, posCenter, size=[200, 200]):
            self.posCenter = posCenter
            self.size = size

        def update(self, cursor):
            cx, cy = self.posCenter
            w, h = self.size

            # If the index finger tip is in the rectangle region
            if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                self.posCenter = cursor

    rectList = []
    for x in range(5):
        rectList.append(DragRect([x * 250 + 150, 150]))

    frameR = 80
    smoothening = 10
    wCam, hCam = 640, 480
    pTime = 0
    cTime = 0

    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    wScr, hScr = pyautogui.size()

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detection_confidence=0.8, max_hands=1)

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    with open("logs_mouse_tracking.log", "a") as f:
        f.write(f"{current_time}: Mouse Tracker Started\n")

    while True:
        try:
            succes, img = cap.read()
            img2 = img.copy()

            img = detector.findHands(img, draw=True)
            lmList, bbox = detector.findPosition(img, draw=True)

            try:
                if len(lmList) > 8:
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]
            except Exception as e:
                pass

            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR,
                                                  hCam - frameR), (255, 0, 255), 2)

            if fingers != []:
                if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    # 5. Convert Coordinates
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    # 6. Smoothen Values
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    # 7. Move Mouse
                    pyautogui.moveTo(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                    now = datetime.now()
                    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

                    with open("logs_mouse_tracking.log", "a") as f:
                        f.write(
                            f"{current_time}: Mouse Cursor Moving using Index Finger running\n")

                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    length, _, lineInfor = detector.findDist(
                        8, 12, img, draw=False)
                    if length < 40:
                        cv2.circle(img, (lineInfor[0], lineInfor[1]),
                                   15, (0, 255, 0), cv2.FILLED)
                        cv2.circle(img, (lineInfor[2], lineInfor[3]),
                                   15, (0, 255, 0), cv2.FILLED)

                        pyautogui.dragTo(wScr - clocX, clocY, button='left')
                        plocX = clocX
                        plocY = clocY

                        now = datetime.now()
                        current_time = now.strftime("%d/%m/%Y %H:%M:%S")

                        with open("logs_mouse_tracking.log", "a") as f:
                            f.write(
                                f"{current_time}: Mouse Right Click using all the 4 Fingers running\n")

                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                    # 9. Find distance between fingers
                    l1, img, lI1 = detector.findDist(8, 12, img, draw=False)
                    l2, _, lI2 = detector.findDist(12, 16, img, draw=False)

                    # print(length)
                    # 10. Click mouse if distance short
                    if l1 < 40 and l2 < 40:
                        cv2.circle(img, (lI1[0], lI1[1]),
                                   15, (0, 0, 255), cv2.FILLED)
                        cv2.circle(img, (lI1[2], lI1[3]),
                                   15, (0, 0, 255), cv2.FILLED)
                        cv2.circle(img, (lI2[2], lI2[3]),
                                   15, (0, 0, 255), cv2.FILLED)
                        pyautogui.click()
                        time.sleep(1)

                        now = datetime.now()
                        current_time = now.strftime("%d/%m/%Y %H:%M:%S")

                        with open("logs_mouse_tracking.log", "a") as f:
                            f.write(
                                f"{current_time}: Mouse Cursor Drag using Index and Middle Finger running\n")

                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    # 9. Find distance between fingers
                    l1, _, lI1 = detector.findDist(8, 12, img, draw=False)
                    l2, _, lI2 = detector.findDist(12, 16, img, draw=False)
                    l3, _, lI3 = detector.findDist(16, 20, img, draw=False)

                    if l1 < 40 and l2 < 40 and l3 < 40:
                        cv2.circle(img, (lI1[0], lI1[1]),
                                   15, (0, 0, 0), cv2.FILLED)
                        cv2.circle(img, (lI1[2], lI1[3]),
                                   15, (0, 0, 0), cv2.FILLED)
                        cv2.circle(img, (lI3[0], lI3[1]),
                                   15, (0, 0, 0), cv2.FILLED)
                        cv2.circle(img, (lI3[2], lI3[3]),
                                   15, (0, 0, 0), cv2.FILLED)

                        pyautogui.click(button='right')
                        time.sleep(1)

                        now = datetime.now()
                        current_time = now.strftime("%d/%m/%Y %H:%M:%S")

                        with open("logs_mouse_tracking.log", "a") as f:
                            f.write(
                                f"{current_time}: Mouse Left Click using Index, Middle and Ring Finger running \n")

            cTime = time.time()
            fps = (1/(cTime - pTime))
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 70),
                        cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)

            cv2.imshow("Image", img)
            # cv2.imshow("Image2", img2)
            if (cv2.waitKey(1)) % 256 == 27:

                now = datetime.now()
                current_time = now.strftime("%d/%m/%Y %H:%M:%S")

                with open("logs_mouse_tracking.log", "a") as f:
                    f.write(f"{current_time}: Program Closed Successfully \n\n")

                break
        except Exception as e:
            now = datetime.now()
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("error.log", "w") as f:
                f.write(f"{current_time}: Error Occured: {e}")

    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("error.log", "w") as f:
        f.write(f"{current_time}: Error Occured: {e}")