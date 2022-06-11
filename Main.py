
from FaceDetection import Detector
from djitellopy import Tello
import time
import cv2
import pygame
import numpy as np


#drone speed
S = 60

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
        self.speed = 10
        self.tello.set_speed(self.speed)

        self.send_rc_control = False
        

    def autonomous_flight(self, screen_dimensions, bboxs):
        #bbox present
        if bboxs:
            bbox = bboxs[0][1][0]
            x, y, w, h = bbox
            x1, y1 = x + w, y + h
            cX, cY = int((x + x1)/2), int((y +y1)/2)
            sX, sY = screen_dimensions
            sX, sY = sX//2, sY//2
        
        else:
            pass


        self.check_inputs()

    def manual_flight(self):
        self.check_inputs()
        
    def check_inputs(self):
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
                self.fb_velocity = S
            elif key == pygame.K_DOWN:  # set backward velocity
                self.fb_velocity = -S
            elif key == pygame.K_LEFT:  # set left velocity
                self.lr_velocity = -S
            elif key == pygame.K_RIGHT:  # set right velocity
                self.lr_velocity = S
            elif key == pygame.K_w:  # set up velocity
                self.ud_velocity = S
            elif key == pygame.K_s:  # set down velocity
                self.ud_velocity = -S
            elif key == pygame.K_q:  # set yaw counter clockwise velocity
                self.yaw_velocity = -S
            elif key == pygame.K_e:  # set yaw clockwise velocity
                self.yaw_velocity = S
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
    

class Mediacontrol(Flightcontrol):
    def __init__(self, tello):
        self.tello = tello
        self.tello.streamon()
        self.pTime = 0
        self.bboxs = []

        #screen dimensions
        img = self.tello.get_frame_read().frame
        self.screen_height, self.screen_width = img.shape[0:2]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stream")


    def start(self, detector):
        img = self.tello.get_frame_read().frame
        img, self.bboxs = detector.detect(img)

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
        cv2.waitKey(10)


    def convert2Pygame(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = np.flipud(img)
        img = pygame.surfarray.make_surface(img)
        self.screen.blit(img, (0,0))
        pygame.display.update()
        time.sleep(1 / FPS)




    



def main():
    detector = Detector(.75)
    drone = Flightcontrol()
    stream = Mediacontrol(drone.tello)

    while drone.run:
        stream.start(detector)
        if not drone.auto:
            drone.manual_flight()
        else:
            drone.autonomous_flight([stream.screen_height, stream.screen_width], stream.bboxs)
    
    drone.tello.land()


if __name__ == "__main__":
    main()