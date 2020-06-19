#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from std_srvs.srv import Empty
import os
from cv_bridge import CvBridge, CvBridgeError


class VideoTalker:

	def __init__(self):
		rospy.init_node('tennis_ball_image', anonymous=True) 

		# declare publisher
		self.videoPublisher = rospy.Publisher('tennis_ball_image', Image, queue_size=10)

		# declare where to capture the video
		self.cvVideoStream = cv2.VideoCapture(os.path.dirname(os.path.abspath(__file__)) + "/video/tennis-ball-video.mp4")

		# publish rate of messages
		self.loopRate = rospy.Rate(30)

		# bridge between ROS and OpenCV
		self.bridge = CvBridge()

	def tennis_ball_publisher(self):
		while not rospy.is_shutdown():
			# read the video stream
			ret, frame = self.cvVideoStream.read()

			if frame is not None:
				try:
					# convert cv to ROS
					ros_frame = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
				except CvBridgeError as e:
					print(e)

				# publish the images to the topic
				self.videoPublisher.publish(ros_frame)
				self.loopRate.sleep()
			else:
				self.cvVideoStream = cv2.VideoCapture(os.path.dirname(os.path.abspath(__file__)) + "/video/tennis-ball-video.mp4")

		self.cvVideoStream.release()



	
if __name__ == '__main__':
	talker = VideoTalker()

	try:
		talker.tennis_ball_publisher()
	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")
		pass