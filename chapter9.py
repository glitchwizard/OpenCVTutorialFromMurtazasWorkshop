#Face Detection
import cv2

faceCascade = cv2.CascadeClassifier('Resources/haarcascades/haarcascade_frontalface_default.xml')
img = cv2.imread('Resources/kam.jpg')

cv2.imshow("Result", img)
cv2.waitKey(0)