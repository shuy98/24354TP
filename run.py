#################################
# Kinect body detection
# from https://github.com/Kinect/PyKinect2
# adapted and modified by Shu You
#################################

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

import time
import math
import serial

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

uno = serial.Serial('COM10', 9600) # enter serial port number here

class BodyGameRuntime(object):
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("24354 Term Project Kinect")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None

        # left hand
        self.prev_left_hand_height = 0
        self.cur_left_hand_height = 0
        self.prev_left_hand_width = 0
        self.cur_left_hand_width = 0
        self.position_left_hand = (0, 0)

        # left shoulder
        self.prev_left_shoulder_height = 0
        self.cur_left_shoulder_height = 0
        self.prev_left_shoulder_width = 0
        self.cur_left_shoulder_width = 0
        self.position_left_shoulder = (0, 0)

        #left elbow
        self.prev_left_elbow_height = 0
        self.cur_left_elbow_height = 0
        self.prev_left_elbow_width = 0
        self.cur_left_elbow_width = 0
        self.position_left_elbow = (0, 0)

        self.left_arm_angle = 0
        self.is_calibrated = False


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    # calculates the position of point_2 relative to point_1
    def calc_position_rel(self, point_1, point_2):
        x_diff = point_2[0] - point_1[0]
        y_diff = point_2[1] - point_1[1]
        return (x_diff, y_diff) # returns a tuple

    # calculates the distance between two points
    def calc_distance(self, point_1, point_2):
        x_diff = point_2[0] - point_1[0]
        y_diff = point_2[1] - point_1[1]
        result = math.sqrt(x_diff**2 + y_diff**2)
        return result

    # calcualtes the dot product between point_1 and point_2
    def calc_dot_product(self, point_1, point_2):
        return point_1[0] * point_2[0] + point_1[1] * point_2[1]

    # calculates angle(1_middle_2)
    def calc_angle(self, point_1, point_middle, point_2):
        point_1_rel = self.calc_position_rel(point_middle, point_1)
        point_2_rel = self.calc_position_rel(point_middle, point_2)
        cos_angle = (self.calc_dot_product(point_1_rel, point_2_rel)/
                    (self.calc_distance(point_middle, point_2) * 
                     self.calc_distance(point_middle, point_1)))
        return math.acos(cos_angle) / math.pi * 180


    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    if body.is_tracked:
                        
                        # if not self.is_calibrated:
                        #     print("waiting for calibration...")
                        #     time.sleep(3)
                        #     print("go")
                        #     self.is_calibrated = True
                        

                        joints = body.joints 

                        
                        # left hand x and y position
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_hand_height = joints[PyKinectV2.JointType_HandLeft].Position.y
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_hand_width = joints[PyKinectV2.JointType_HandLeft].Position.x
                        self.position_left_hand = (self.cur_left_hand_width, self.cur_left_hand_height)

                        # left shoulder x and y position
                        if joints[PyKinectV2.JointType_ShoulderLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_shoulder_height = joints[PyKinectV2.JointType_ShoulderLeft].Position.y
                        if joints[PyKinectV2.JointType_ShoulderLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_shoulder_width = joints[PyKinectV2.JointType_ShoulderLeft].Position.x
                        self.position_left_shoulder = (self.cur_left_shoulder_width, self.cur_left_shoulder_height)

                        # left elbow x and y position
                        if joints[PyKinectV2.JointType_ElbowLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_elbow_height = joints[PyKinectV2.JointType_ElbowLeft].Position.y
                        if joints[PyKinectV2.JointType_ElbowLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                            self.cur_left_elbow_width = joints[PyKinectV2.JointType_ElbowLeft].Position.x
                        self.position_left_elbow = (self.cur_left_elbow_width, self.cur_left_elbow_height)

                        self.left_arm_angle = self.calc_angle(self.position_left_hand, self.position_left_elbow, 
                                                         self.position_left_shoulder)

                        
                        if (self.left_arm_angle <= 90):
                            #print("left_arm_angle is less than 90 degrees")
                            msg = 'o'
                            uno.write(msg.encode())
                            #uno.write(b'turn on led')                            
                            #print(msg.encode())
                            #line = uno.readline()
                            #print(line)
                        else:
                            #print("left_arm_angle is not less than 90 degrees")
                            msg = 'c'
                            uno.write(msg.encode())
                            #uno.write(b'turn off led')
                            #print(msg.encode())
                            #line = uno.readline()
                            #print(line)

                        #self.prev_left_hand_height = self.cur_left_hand_height



                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();

