import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(-1)
cap.set(3, 1280)
cap.set(4, 720)
colorR = 0, 0, 255
color = 255, 0, 0
x, y = 300, 300
w, h = 350, 325
detector = HandDetector(detectionCon=0.8, maxHands=2)


class DragReact():
    def __init__(self, posCenter, size=[150,50]):
        self.posCenter = posCenter = posCenter
        self.size = size

    def update(self, cursor):
        x, y = self.posCenter
        w, h = self.size
        if x - w // 2 < cursor[0] < x + w // 2 and y - h // 2 < cursor[1] < y + h // 2:
            self.posCenter = cursor


rectList = []
for x in range(3):
    rectList.append(DragReact([300, x*90+300]))

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hands, frame = detector.findHands(frame)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint = hand1["center"]
        cursor = lmList1[8]
        finger = detector.fingersUp(hand1)
        length, info, img = detector.findDistance(lmList1[8], lmList1[12], frame)
        print(length)
        if length < 90:
            for rect in rectList:
                rect.update(cursor)

        else:
            color = (255, 0, 0)
    for rect in rectList:
        x, y = rect.posCenter
        w, h = rect.size
        cv2.rectangle(frame, (x - w // 2, y - h // 2), (x + w // 2, y + w // 2), color, cv2.FILLED)
        #cvzone.cornerRect(frame,(x-w//2,y-h//2,w,h),20,rt=0)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)
