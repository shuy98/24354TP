self.position_left_hand = self.joint_x_y_pos(joints, PyKinectV2.JointType_HandLeft)

                        # self.position_left_shoulder = self.joint_x_y_pos(joints, PyKinectV2.JointType_ShoulderLeft)

                        # self.position_left_elbow = self.joint_x_y_pos(joints, PyKinectV2.JointType_ElbowLeft)

                        # if (self.position_left_hand == False or 
                        #     self.position_left_elbow == False or
                        #     self.position_left_shoulder == False):
                        #     self.left_arm_angle = 180
                        # else:
                        #     self.left_arm_angle = self.calc_angle(self.position_left_hand, self.position_left_elbow, self.position_left_shoulder)