import cv2
import numpy as np

img = cv2.imread("Resources\cards.jpg")

pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])

cv2.imshow("Image", img)

cv2.waitKey(0)