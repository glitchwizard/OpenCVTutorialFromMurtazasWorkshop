import cv2

frameWidth = 640
frameHeight = 480
licensePlatesCascade = cv2.CascadeClassifier('Resources/haarcascades/haarcascade_russian_plate_number.xml')
minArea = 500
color = (0, 0, 255)


captureDevice = cv2.VideoCapture(0)
captureDevice.set(3, frameWidth)
captureDevice.set(4, frameHeight)
captureDevice.set(10, 160)
count = 0


while True:
    success, img = captureDevice.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # the second and third parameters can change depending in the results we're getting
    licensePlates = licensePlatesCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in licensePlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "License Plate", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1,  color, 2)
            imgRegionOfInterest = img[y:y+h, x:x+w]
            cv2.imshow("RegionOfInterest", imgRegionOfInterest)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Resources/Scanned/LicensePlate_"+ str(count) + ".jpg", imgRegionOfInterest)
        cv2.rectangle(img,(0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1

