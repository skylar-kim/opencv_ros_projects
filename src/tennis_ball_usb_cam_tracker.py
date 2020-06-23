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
    # initialize node for reading from usb camera
    rospy.init_node('ball_cam_tracker', anonymous=True)

    # subscribe to the topic where the usb camera footage is published
    self.videoSub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)

    # so we can use the BallTracker class
    self.tracker = BallTracker()

    # make a bridge object that makes the transformation between ROS and OpenCV formats
    self.bridge = CvBridge()



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
    self.tracker.draw_ball_contour(cv_image, contours)

    cv2.imshow("CV Stream", cv_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      self.videoSub.unregister()
      rospy.signal_shutdown("Exit Code")

def main():
  listener = VideoListener()

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Exit")

if __name__ == '__main__':
    main()