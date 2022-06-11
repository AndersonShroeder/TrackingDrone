import cv2
import mediapipe as mp

class Detector():
    def __init__(self, minDetectionConfidence=0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(minDetectionConfidence)
    
    def detect(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceDetection.process(imgRGB)
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
