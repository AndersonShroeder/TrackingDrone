import cv2
import mediapipe as mp
import time

class HandTracking:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.tipIds = [4, 8, 12, 16, 20]
        self.mpDraw = mp.solutions.drawing_utils
        

    def hand_track(self, img):
        self.results = self.hands.process(img)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

    def hand_position(self, img):
        img = self.hand_track(img)
        lmList = self.findPosition(img, draw=False)
        fingers = []

        if len(lmList) != 0:         
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
                fingers.append(1)

            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return img, fingers
