import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

myColors = [
                [5, 107, 0, 19, 255, 255, "Orange"], #orange
                [133, 56, 0, 159, 156, 255, "Purple"], #purple
                [57, 76, 0, 100, 255, 255, "Green"]  #green
            ]


def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for color in myColors:
        # lower = np.array([h_min, s_min, v_min])
        # upper = np.array([h_max, s_max, v_max])

        lower = np.array(color[0:3])
        upper = np.array(color[3:6])

        mask = cv2.inRange(imgHSV, lower, upper)
        cv2.imshow(str(color[6]), mask)

while True:
    success, img = cap.read()
    findColor(img, myColors)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


