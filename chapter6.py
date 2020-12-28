import cv2
import numpy as np
img = cv2.imread("Resources\kam.jpg")

imgHor = np.hstack((img, img))
imgVert = np.vstack((img,img))

cv2.imshow("Horizontal", imgHor)
cv2.imshow("Vertical", imgVert)

cv2.waitKey(0)