import cv2
import numpy as np
from chapter6 import stackImages

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        #print(area)
        if area > 500:
            cv2.drawContours(imgContour, contour, -1, [255,0,255], 3)
            perimeter = cv2.arcLength(contour, True)
            approximate_corner_points = cv2.approxPolyDP(contour, 0.02*perimeter, True)

            corners = len(approximate_corner_points)
            x, y, w, h = cv2.boundingRect(approximate_corner_points)

            if corners == 3: objectType = "Triangle"
            elif corners == 4:
                aspectRatio = w/float(h)
                if aspectRatio > 0.95 and aspectRatio < 1.05: objectType = "Square"
                else: objectType = "Rectangle"
            elif corners > 4:
                objectType = "Circle"
            else: objectType = "None"


            #this is how a bounding box is drawn
            cv2.rectangle(imgContour,(x,y),(x+w, y+h), (0,255,0), 2)
            cv2.putText(imgContour, objectType, (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 100), 2)




path = 'Resources/shapes.png'
img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)

getContours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8, ([img, imgGray, imgBlur],
                             [imgCanny, imgContour, imgBlank]))

cv2.imshow("Stack", imgStack)
cv2.waitKey(0)

