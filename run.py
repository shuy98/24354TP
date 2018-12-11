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

uno = serial.Serial('COM12', 9600) # enter serial port number here

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

        #self.left_arm_angle = 0
        #self.is_calibrated = False


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState
        joint1State = joints[joint1].TrackingState

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
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft)
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight)

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft)

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight)

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft)
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft)


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

    # find x y position of a joint
    def joint_x_y_pos(self, joints, JointType):
        if joints[JointType].TrackingState != PyKinectV2.TrackingState_NotTracked:
            joint_height = joints[JointType].Position.y
            joint_width = joints[JointType].Position.x
            return (joint_width, joint_height)
        else:
            return False

    def eval_gesture_angle(self, joints, joint_pos_1, joint_pos_2, joint_pos_3):
        pos_1 = self.joint_x_y_pos(joints, joint_pos_1)
        pos_2 = self.joint_x_y_pos(joints, joint_pos_2)
        pos_3 = self.joint_x_y_pos(joints, joint_pos_3)
        angle = 180
        if (pos_1 == False or pos_2 == False or pos_3 == False):
            angle = 180
        else:
            angle = self.calc_angle(pos_1, pos_2, pos_3)
        return angle
    
    def is_hand_closed(self, left_hand_pos, right_hand_pos):
        self.x_diff_hand = self.left_hand_pos[0] - self.right_hand_pos[0]
        self.y_diff_hand = self.left_hand_pos[1] - self.right_hand_pos[1]
        self.pos_diff_hand = ((self.x_diff_hand)**2 + (self.y_diff_hand)**2)**0.5
        if (self.pos_diff_hand < 0.1):
            return True
        else:
            return False

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

            # --- Getting frames and drawing  
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
                        joints = body.joints 

                        self.left_arm_angle = self.eval_gesture_angle(joints, 
                            PyKinectV2.JointType_HandLeft, 
                            PyKinectV2.JointType_ElbowLeft,
                            PyKinectV2.JointType_ShoulderLeft)

                        self.right_arm_angle = self.eval_gesture_angle(joints, 
                            PyKinectV2.JointType_HandRight, 
                            PyKinectV2.JointType_ElbowRight,
                            PyKinectV2.JointType_ShoulderRight)

                        self.left_leg_angle = self.eval_gesture_angle(joints, 
                            PyKinectV2.JointType_FootLeft, 
                            PyKinectV2.JointType_KneeLeft,
                            PyKinectV2.JointType_HipLeft)

                        self.right_leg_angle = self.eval_gesture_angle(joints, 
                            PyKinectV2.JointType_FootRight, 
                            PyKinectV2.JointType_KneeRight,
                            PyKinectV2.JointType_HipRight)

                        self.left_hand_pos = self.joint_x_y_pos(joints, 
                                                PyKinectV2.JointType_HandLeft)

                        self.right_hand_pos = self.joint_x_y_pos(joints, 
                                                PyKinectV2.JointType_HandRight)

                        # if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                        joint_depth = joints[PyKinectV2.JointType_HandLeft].Position.z

                        joint_depth_2 = joints[PyKinectV2.JointType_ShoulderLeft].Position.z

                        if (joint_depth - joint_depth_2 > 0.2 and 
                            self.right_arm_angle > 90):
                            # move backward
                            msg = 's'
                            uno.write(msg.encode())

                        elif (joint_depth - joint_depth_2 < -0.45 and    
                              self.right_arm_angle > 90):
                            # move forward
                            msg = 'w'
                            uno.write(msg.encode())

                        elif (self.left_arm_angle <= 90 and 
                              self.right_arm_angle > 90 and 
                              joints[PyKinectV2.JointType_HandLeft].Position.y >
                        joints[PyKinectV2.JointType_ShoulderLeft].Position.y):
                            msg = 'a'
                            uno.write(msg.encode())
                            
                        elif (self.right_arm_angle <= 90 and 
                              self.left_arm_angle > 90 and 
                              joints[PyKinectV2.JointType_HandRight].Position.y >
                        joints[PyKinectV2.JointType_ShoulderRight].Position.y):
                            msg = 'd'
                            uno.write(msg.encode())

                        elif (self.is_hand_closed(self.left_hand_pos, self.right_hand_pos)
                              and joints[PyKinectV2.JointType_HandLeft].Position.x <
                        joints[PyKinectV2.JointType_Head].Position.x):
                            msg = 'o'
                            uno.write(msg.encode())

                        elif (self.is_hand_closed(self.left_hand_pos, self.right_hand_pos)
                              and joints[PyKinectV2.JointType_HandLeft].Position.x >=
                        joints[PyKinectV2.JointType_Head].Position.x):
                            msg = 'c'
                            uno.write(msg.encode())

                        elif (self.left_leg_angle <= 135):
                            msg = 'l'
                            uno.write(msg.encode())

                        elif (self.right_leg_angle <= 135):
                            msg = 'r'
                            uno.write(msg.encode())

                        else:
                            msg = 't'
                            uno.write(msg.encode())

                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height))
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
game = BodyGameRuntime()
game.run()

