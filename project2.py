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
    imgCanny = cv2.Canny(imgBlur, 100, 150)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations= 2)
    imgThreshold = cv2.erode(imgDialation, kernel, iterations=1)

    return imgThreshold

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        #print(area)
        if area > 5000:
            cv2.drawContours(imgContour, contour, -1, [255,0,255], 3)
            perimeter = cv2.arcLength(contour, True)
            approximate_corner_points = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            if area > maxArea and len(approximate_corner_points) == 4:
                biggest = approximate_corner_points

                #this will replace whatever area it has found before with the bigger area until it finds the max area
                maxArea = area
    return biggest

    # corners = len(approximate_corner_points)
    # x, y, w, h = cv2.boundingRect(approximate_corner_points)


#function stackImages provided by Murtaza's Workshop
def stackImages(scale,imgArray):
    rows = len(imgArray)
    columns = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range (0, columns):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range (0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = captureDevice.read()
    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()
    imgThreshold = preProcessing(img)
    getContours(imgThreshold)
    cv2.putText(img, "Webcam", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)
    cv2.putText(imgThreshold, "PreProcessed", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)
    cv2.putText(imgContour, "Contour", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)

    imgStack = stackImages(0.8, ([img, imgThreshold, imgContour]))

    cv2.imshow("Image stack", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

