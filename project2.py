import cv2
import numpy as np

#Document Scanner using OpenCV

widthImg = 480
heightImg = 640

captureDevice = cv2.VideoCapture(0)
captureDevice.set(3, widthImg)
captureDevice.set(4, heightImg)
captureDevice.set(10, 160)

def empty(a):
    pass

cv2.namedWindow("Capture Parameters")
cv2.resizeWindow("Capture Parameters", 640, 100)
cv2.createTrackbar("Canny Min Threshold", "Capture Parameters", 25, 255, empty)
cv2.createTrackbar("Canny Max Threshold", "Capture Parameters", 90, 255, empty)

#TODO: refactor so things actually make sense

def getImgCanny(img, min, max):
    return cv2.Canny(img, min, max)

def convertImgToGrayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blurImage(img):
    return cv2.GaussianBlur(img, (5, 5), 1)

def preProcessing(img):
    imgGray = convertImgToGrayscale(img)
    imgBlur = blurImage(imgGray)
    imgCanny = getImgCanny(imgBlur, canny_min_threshold, canny_max_threshold)
    kernel = np.ones((5, 5))
    imgDialation = cv2.dilate(imgCanny, kernel, iterations= 3)
    imgThreshold = cv2.erode(imgDialation, kernel, iterations=3)
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
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest

    # corners = len(approximate_corner_points)
    # x, y, w, h = cv2.boundingRect(approximate_corner_points)

def reorderPointsForWarpOptimization(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)

    #take the minimum value point and set it as the first index
    myPointsNew[0] = myPoints[np.argmin(add)]
    #take the maximum value point and set it as the last index
    myPointsNew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis = 1)
    #find the second highest and lowest points, and set them where they need to go.
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew



def getWarp(img, biggest):
    #the points don't come in with the right orientation, so we need to reorder them to warp properly
    biggest = reorderPointsForWarpOptimization(biggest)
    print("biggestshape:",biggest.shape)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    return imgOutput


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

    canny_min_threshold = cv2.getTrackbarPos("Canny Min Threshold","Capture Parameters")
    canny_max_threshold = cv2.getTrackbarPos("Canny Max Threshold","Capture Parameters")

    imgThreshold = preProcessing(img)

    biggest = getContours(imgThreshold)

    print(biggest)
    imgGray = convertImgToGrayscale(img)
    imgBlur = blurImage(imgGray)
    imgCanny = getImgCanny(imgBlur, canny_min_threshold, canny_max_threshold)

    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        cv2.putText(img, "Webcam", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)
        cv2.putText(imgThreshold, "PreProcessed", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)
        cv2.putText(imgContour, "Contour", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 100, 100), 2)
        zeroImg = np.zeros_like(img)

        imageArray = ([img, imgThreshold, imgContour],
                             [imgWarped, imgCanny, zeroImg])

    else: imageArray = ([img, imgCanny, imgContour])

    imgStack = stackImages(0.8, imageArray)

    cv2.imshow("Image stack", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

