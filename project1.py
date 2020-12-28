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
        x, y = getContours(mask)
        cv2.circle(imgResult,(x,y), 10, (255,0,0), cv2.FILLED)
        #cv2.imshow(str(color[6]), mask)

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0, 0, 0, 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            cv2.drawContours(imgResult, contour, -1, [255,0,255], 3)
            perimeter = cv2.arcLength(contour, True)
            approximate_contour = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approximate_contour)

    return x+w//2, y

while True:
    success, img = cap.read()
    imgResult = img.copy()
    findColor(img, myColors)
    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


