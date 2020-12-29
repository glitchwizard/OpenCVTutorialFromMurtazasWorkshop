import cv2
import numpy as np

#Document Scanner using OpenCV

widthImg = 640
heightImg = 480

captureDevice = cv2.VideoCapture(0)
captureDevice.set(3, widthImg)
captureDevice.set(4, heightImg)
captureDevice.set(10, 140)

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations= 2)
    imgThreshold = cv2.erode(imgDialation, kernel, iterations=1)

    return imgThreshold

while True:
    success, img = captureDevice.read()
    img = cv2.resize(img, (widthImg, heightImg))
    imgThreshold = preProcessing(img)
    cv2.imshow("PreProcessed", imgThreshold)
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

