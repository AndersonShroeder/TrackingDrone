import cv2
import mediapipe as mp
import numpy as np


class Detector:
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils

    def draw(self, img, bbox, l = 30, t = 5):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cX, cY = int((x + x1)/2), int((y +y1)/2)

        cv2.rectangle(img, bbox, (255, 0, 255), 1) #draw smaller box

        #top left
        cv2.line(img, (x, y), (x+l,y), (255, 0, 255), t) #draw thicker line
        cv2.line(img, (x, y), (x,y+l), (255, 0, 255), t)

        #top right
        cv2.line(img, (x1, y), (x1-l,y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1,y+l), (255, 0, 255), t)

        #bottom right
        cv2.line(img, (x1, y1), (x1-l,y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1,y1-l), (255, 0, 255), t)

        #bottom left
        cv2.line(img, (x, y1), (x+l,y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x,y1-l), (255, 0, 255), t)

        cv2.circle(img, (cX,cY), 4, (0,255,0), 2)

        return img
        
thres = 0.65 # Threshold to detect object
 
class Objdetector(Detector):
    def __init__(self, configPath = 'ObjectDetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt', modelPath = 'ObjectDetection/frozen_inference_graph.pb', classesPath = 'ObjectDetection/coco.names'):
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClaseses()

    def readClaseses(self):
        with open(self.classesPath, 'rt') as f:
            self.classesList = f.read().rstrip('\n').split('\n')

        self.classesList.insert(0, '__Background__')

    def run(self, img):
        classLabelIDs, confidences, bboxs = self.net.detect(img, confThreshold=thres)
    
        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1,-1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = .5, nms_threshold = .2)

        #loop through all non overlapping boxes
        if len(bboxIdx) != 0:
            for i in range(0, len(bboxIdx)):

                bbox = bboxs[np.squeeze(bboxIdx[i])]
                classConfidence = confidences[np.squeeze(bboxIdx[i])]
                classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                classLabel = self.classesList[classLabelID]

                displayText = "{}:{:.4f}".format(classLabel, classConfidence)

                x, y, w, h = bbox

                cv2.putText(img, displayText, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1 , (0, 255, 0), 1)
                self.draw(img, bbox)
            
        return img, bboxs

class Handtracking(Detector):
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.tipIds = [4, 8, 12, 16, 20]
        

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

    def run(self, img):
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

class Facedetector(Detector):
    def __init__(self, minDetectionConfidence=0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(minDetectionConfidence)

    def run(self, img):
        results = self.faceDetection.process(img)
        bboxs = []

        if results.detections:
            #iterates through the resulting detections providing id and the detection class
            for id, detection in enumerate(results.detections):
                #mpDraw.draw_detection(img, detection)

                #use detection class to draw bounding box onto img
                bboxC = detection.location_data.relative_bounding_box #
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                bboxs.append([id, [bbox], detection.score])
                self.draw(img, bbox)

                #print confidence score
                cv2.putText(img, f"{int(detection.score[0] * 100)}%", (bbox[0], bbox[1] - 20), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        
        return img, bboxs
    
