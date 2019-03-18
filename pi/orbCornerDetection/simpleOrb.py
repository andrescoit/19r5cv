import numpy as np
import cv2
import matplotlib as plt

img = cv2.imread('square.jpg', 0)

#Initiate STAR detector
orb = cv2.ORB()

#find the keypoints with ORB
lp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

#draw onl keypoints location, not size and orientation
img2 = cv2.drawKeypoints(img,kp,color(0,255,0), flags=0)
plt.imshow(img2), plt.show()
