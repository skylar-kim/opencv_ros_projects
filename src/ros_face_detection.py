#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class VideoStreamer:
    def __init__(self):
        # Initialize node for reading from webcam
        rospy.init_node('ros_face_detection', anonymous=True)

        # Subscribe to the topic where the usb camera footage is published
        self.videoSub = rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)

        # Make a bridge object that makes the transformations between ROS and OpenCV formats
        self.bridge = CvBridge()


    def image_callback(self, ros_image):
    	print 'got an image'
        global face_cascade
        
        #convert ros_image into an opencv-compatible image
        try:
            cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError as e:
            print(e)

        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display
        cv2.imshow('CV Stream', cv_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.videoSub.unregister()
            rospy.signal_shutdown("Exit Code")


def main():
    

    streamer = VideoStreamer()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("exit")


if __name__ == '__main__':
    main()

