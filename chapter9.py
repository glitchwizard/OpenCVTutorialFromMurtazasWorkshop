#Face Detection
import cv2

faceCascade = cv2.CascadeClassifier('Resources/haarcascades/haarcascade_frontalface_default.xml')
img = cv2.imread('Resources/kam.jpg')
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #the second and third parameters can change depending in the results we're getting
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

#Cascade methods can be used to detect faces, or any object, and you can create your own cascades
#This method is not the most accurate, but it's fast

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow("Result", img)
cv2.waitKey(0)