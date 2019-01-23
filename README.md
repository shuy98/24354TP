# Semi-Autonomous Omnidirectional Manipulation Robot 
Term project for course 24-354 Gadgetry: Sensors, Actuators, and Processors at Carnegine Mellon University.  
This is a team project by Shu You, Nikhila Vembu, and Hardik Singh.
Any questions/comments or you want additional info please send me an email: shuy@andrew.cmu.edu 

## Description
We created a small, moveable, omnidirectional robot that will be controlled virtually using a Kinect. We will demonstrate control of the robot and the ability to accomplish a terrain manipulation task with the robot by using a series of arm/hand gestures to command the robot’s movement and use of its gripper. The task will consist of retrieving an object and returning it into and ending spot based on the way we direct it with our bodies. The robot will ideally have to navigate through a few obstacles and then reach a box which senses that the robot arrived with the object.

![alt text](https://github.com/shuy98/24354TP/blob/master/presentation/img/cad_collage.JPG)
*Fig 1. Robot CAD Image*

![alt text](https://github.com/shuy98/24354TP/blob/master/img/assembly.jpg)
*Fig 2. Robot Final Assembly*

![alt text](https://github.com/shuy98/24354TP/blob/master/presentation/img/vlcsnap-2018-12-11-11h48m14s029.png)
*Fig 3. Kinect Control Interface*

## Problem Statement
We are aiming to display and test how well we can control unmanned robots and drones better with our bodies. 
Where "gaming controllers" are limited by their buttons, we can move our body more precisely and in a greater variety of ways, giving us access to improved ways of controlling the robot.

## Electronic Components
- Microprocessors 
  - Two Arduino UNO
- Actuators 
  - Three DC motors
  - One gripper with DC motor
- Sensors
  - Two Elegoo HC-SR04 proximity sensors
  - Microsoft Kinect

![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture8.jpg)

*Fig 4. Main Circuit Schematics*
  
## Kinect
Read body joints and save in (x, y, z) coordinates. Do calculations based on joints coordinates.
  
![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture3.png)

*Fig 5. Gesture diagram*

- Take (x, y) coordinates of points A, B, and C.
- Use Pythagorean Theorem to calculate AB and BC.
- Use dot product to calculate the angle θ.
- We designed 8 gestures.

![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture4.png)

*Fig 6. Kinect Code Flowchart*

Kinect reads gesture and maps the gesture to a unique ID, then it sends the ID to serial port. 

## Robot Design and Motion Design

We used balsa wood as the base plate and we used laser cutter to cut the plate. We also chose omniwheels to allow the robot to move and rotate in any directions. A small DC motor equipped gripper is integrated to the robot, so it can pick up objects.

![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture9.png)
![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture11.jpg)

*Fig 7. Robot design process and robot picking up object*

![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture5.jpg)

*Fig 8. Robot Motion Diagram*

![alt text](https://github.com/shuy98/24354TP/blob/master/img/Picture6.png)

*Fig 9. Robot(Arduino) Code Flowchart*

Robot motion is based on different spinning speeds of three DC motors. For example, if we want the robot to move forward, we spind left wheel forward and right wheel backward while keeping the third wheel fixed.

- Arduino reads ID from serial port. 
- Maps ID to a specific motion helper function (e.g. moveForward()).
- Execute motion and wait for next incoming ID.
- 8 gestures map to 8 motions.

  
## Video Demo on Wirelessly Control the Robot
https://drive.google.com/file/d/1rcVZQeMSRfaizCOLsIZgg6IILubUMUVS/view?usp=sharing

## Additional Info
Check project proposal and project progress reports for more details.  
Project Proposal: https://github.com/shuy98/24354TP/blob/master/Project%20Proposal.pdf  
Progress 1 report: https://github.com/shuy98/24354TP/blob/master/Progress%20Update%201-2.pdf  
Progress 2 report: https://github.com/shuy98/24354TP/blob/master/Progress%20Update%202.pdf  
