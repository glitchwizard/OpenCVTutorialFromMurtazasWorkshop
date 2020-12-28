import cv2

#Document Scanner using OpenCV

frameWidth = 640
frameHeight = 480
captureDevice = cv2.VideoCapture(0)
captureDevice.set(3, frameWidth)
captureDevice.set(4, frameHeight)
captureDevice.set(10, 130)

while True:
    success, img = captureDevice.read()
    cm2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

