#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ball_tracker import BallTracker
import sys

class VideoListener:
  
  def __init__(self):
    # initialize node
    rospy.init_node('tennis_ball_image', anonymous=True)

    # make a bridge object that makes the transformation between ROS and OpenCV formats
    self.bridge = CvBridge()

    # so we can use the BallTracker class
    self.tracker = BallTracker()

  def tennis_ball_listener(self):

    image_sub = rospy.Subscriber("/tennis_ball_image",Image, self.image_callback)
    try:
      rospy.spin()
    except KeyboardInterrupt:
      print("Shutting down")
      pass

  def image_callback(self, ros_image):
    print 'got an image'

    #convert ros_image into an opencv-compatible image
    try:
      cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
    except CvBridgeError as e:
      print(e)

    # define yellow upper and lower bounds
    yellowLower =(30, 150, 100)
    yellowUpper = (50, 255, 255)

    # turn the cv_image frame into a binary image
    binary_image_mask = self.tracker.filter_color(cv_image, yellowLower, yellowUpper)

    # get the contours from the binary image
    contours = self.tracker.getContours(binary_image_mask)

    # draw the contours on the ball
    self.tracker.draw_ball_contour(binary_image_mask, cv_image, contours)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      rospy.signal_shutdown("Exit Code")


if __name__ == '__main__':
    listener = VideoListener()
    listener.tennis_ball_listener()