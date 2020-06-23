#!/usr/bin/env python

import cv2
import rospy
import numpy as np



class BallTracker:

    # methods to do the ball detection algorithm
    def filter_color(self, rgb_image, lower_bound_color, upper_bound_color):
        #convert the image into the HSV color space
        hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)

        #define a mask using the lower and upper bounds of the yellow color 
        mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)

        return mask

    def getContours(self, binary_image):
        _, contours, hierarchy = cv2.findContours(binary_image.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def draw_ball_contour(self, rgb_image, contours):
        #black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')

        for c in contours:
            area = cv2.contourArea(c)
            perimeter= cv2.arcLength(c, True)
            
            if (area>100):
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
                #cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
                cx, cy = self.get_contour_center(c)
                cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
                #cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
                #cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)

        #cv2.imshow("RGB Image Contours",rgb_image)
        #cv2.imshow("Black Image Contours",black_image)

    def get_contour_center(self, contour):

        M = cv2.moments(contour)
        cx=-1
        cy=-1
        if (M['m00']!=0):
            cx= int(M['m10']/M['m00'])
            cy= int(M['m01']/M['m00'])
        return cx, cy
