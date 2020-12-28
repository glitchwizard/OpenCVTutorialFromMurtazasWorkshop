import cv2
import numpy as np
from chapter6 import stackImages

path = 'Resources/shapes.png'
img = cv2.imread(path)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.6, ([img, imgGray, imgBlur],
                             [imgCanny, imgBlank, imgBlank]))

cv2.imshow("Stack", imgStack)
cv2.waitKey(0)

