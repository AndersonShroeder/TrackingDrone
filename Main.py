
from FaceDetection import Detector
from HandTracking import HandTracking
from djitellopy import Tello
from math import sqrt
import time
import cv2
import pygame
import numpy as np


#drone speed


FPS = 120

class Flightcontrol():
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.run = True
        self.auto = False #intializes drone as manual flight

        self.fb_velocity = 0 #Forward(+) -back(-)
        self.ud_velocity = 0 #Up(+) -Down(-)
        self.lr_velocity = 0 #Left(+) - Right(-)
        self.yaw_velocity = 0
        self.S = 60 #Drone default adjust speed
        self.speed = 10
        self.tello.set_speed(self.speed)
        self.hand_signals = []

        self.send_rc_control = False
    
    def change_speed(self, target_pixel, current_pixel):
        self.S = int(60-(60/(2**((target_pixel/current_pixel) - 1))))
        return self.S

    def check_yaw(self, cX, sX, error):
        if (cX + error) < sX or (cX + error) > sX:
            self.yaw_velocity = self.change_speed(cX, sX)

    
    def check_ud(self, cY, sY, error):
        if (cY + error) < sY or (cY + error) > sY:
            self.ud_velocity = self.change_speed(cY, sY)

    def check_fb(self, w, h, screen_dimensions, ratio):
        sX, sY = screen_dimensions
        box_area = w * h
        screen_area = sX * sY
        acceptable_area = (sX * ratio) * (sY * ratio)
        if (box_area) < acceptable_area or (box_area) > acceptable_area:
            self.fb_velocity = -self.change_speed(sqrt(box_area), sqrt(acceptable_area))


        
    def autonomous_flight(self, screen_dimensions, bboxs, error = 10):

        #bbox present
        if bboxs:
            bbox = bboxs[0][1][0]
            x, y, w, h = bbox
            x1, y1 = x + w, y + h
            cX, cY = int((x + x1)/2), int((y +y1)/2)
            sX, sY = screen_dimensions
            sY = sY//4
            sX = sX//2
            print(sY, cY)

            #check yaw
            self.check_yaw(cX, sX, 5)
            
            #check up/down - swapped target/current
            self.check_ud(sY, cY, 5)

            self.check_fb(w, h, screen_dimensions, 1/2)

            #send adjustments to drone
            self.update()

            #reset velocities
            self.ud_velocity, self.lr_velocity, self.yaw_velocity, self.fb_velocity = 0, 0 ,0 ,0
            self.update()

        else:
            pass

 
        self.check_inputs()


    def manual_flight(self):
        self.check_inputs()
        
    def check_hands(self):
        if self.hand_signals:
            if self.hand_signals== [0, 1, 0, 0, 0]:
                self.auto = True
            if self.hand_signals == [0, 1, 1, 0, 0]:
                self.auto = False
        else:
            pass

    def check_inputs(self):
        self.check_hands()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                else:
                    self.key_down(event.key)
                    self.update()
            elif event.type == pygame.KEYUP:
                self.key_up(event.key)
                self.update()

    def key_down(self, key):
        if not self.auto:
            if key == pygame.K_UP:  # set forward velocity
                self.fb_velocity = self.S
            elif key == pygame.K_DOWN:  # set backward velocity
                self.fb_velocity = -self.S
            elif key == pygame.K_LEFT:  # set left velocity
                self.lr_velocity = -self.S
            elif key == pygame.K_RIGHT:  # set right velocity
                self.lr_velocity = self.S
            elif key == pygame.K_w:  # set up velocity
                self.ud_velocity = self.S
            elif key == pygame.K_s:  # set down velocity
                self.ud_velocity = -self.S
            elif key == pygame.K_q:  # set yaw counter clockwise velocity
                self.yaw_velocity = -self.S
            elif key == pygame.K_e:  # set yaw clockwise velocity
                self.yaw_velocity = self.S
            elif key == pygame.K_a:
                self.auto = True
        else:
            if key == pygame.K_m:
                self.auto = False

    def key_up(self, key):
        if not self.auto:
            if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
                self.fb_velocity = 0
            elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
                self.lr_velocity = 0
            elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
                self.ud_velocity = 0
            elif key == pygame.K_q or key == pygame.K_e:  # set zero yaw velocity
                self.yaw_velocity = 0
            elif key == pygame.K_t:  # takeoff
                self.tello.takeoff()
                self.send_rc_control = True
            elif key == pygame.K_l:  # land
                not self.tello.land()
                self.send_rc_control = False
        else:
            if key == pygame.K_t:  # takeoff
                self.tello.takeoff()
                self.send_rc_control = True
            elif key == pygame.K_l:  # land
                not self.tello.land()
                self.send_rc_control = False

    def update(self):
        if self.send_rc_control:
            self.tello.send_rc_control(self.lr_velocity, self.fb_velocity,
                self.ud_velocity, self.yaw_velocity)
    
class DetectorMerge:
    def __init__(self, face_detector = False, hand_tracker = False):
        self.fd = face_detector
        self.ht = hand_tracker
        self.hand_tracker = None
        self.face_detector = None

        if face_detector:
            self.create_FD()
            self.fd = True
        if hand_tracker:
            self.create_HT()
            self.ht = True

    def create_HT(self):
        self.hand_tracker = HandTracking()

    def create_FD(self):
        self.face_detector = Detector(.75)

    


class Mediacontrol(Flightcontrol):
    def __init__(self, tello):
        self.tello = tello
        self.tello.streamoff()
        self.tello.streamon()
        self.pTime = 0
        self.bboxs = []
        self.hands = []
        self.landmark_locations = []

        #screen dimensions
        img = self.tello.get_frame_read().frame
        self.screen_height, self.screen_width = img.shape[0:2]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stream")


    def start(self, detector):
        img = self.tello.get_frame_read().frame
        if detector.fd:
            img, self.bboxs = detector.face_detector.detect(img)
        if detector.ht:
            img, self.hands = detector.hand_tracker.hand_position(img)
  
        #Display Fps
        cTime = time.time()
        fps = 1/(cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        #Draw Center Circle
        h, w, c= img.shape
        cY = h//2
        cX = w//2
        cv2.circle(img, (cX, cY), 4, (0,255,0), 2)
        
        #convert cv2 frame to pygame window
        self.convert2Pygame(img)

        #cv2.imshow("Image", img)
        cv2.waitKey(1)


    def convert2Pygame(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = np.flipud(img)
        img = pygame.surfarray.make_surface(img)
        self.screen.blit(img, (0,0))
        pygame.display.update()
        time.sleep(1 / FPS)




    



def main():
    detector = DetectorMerge(True, True)
    drone = Flightcontrol()
    stream = Mediacontrol(drone.tello)

    while drone.run:
        stream.start(detector)
        drone.hand_signals = stream.hands
        if not drone.auto:
            drone.manual_flight()
        else:
            drone.autonomous_flight([stream.screen_height, stream.screen_width], stream.bboxs)
    
    drone.tello.land()


if __name__ == "__main__":
    main()