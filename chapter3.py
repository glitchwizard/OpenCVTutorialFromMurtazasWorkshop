import cv2
import numpy as np

img = cv2.imread("Resources/lambo.webp")
print(img.shape)

imgResize = cv2.resize(img, (300,200))

imgCropped = img[600:1000, 500:800]

cv2.imshow("Image",img)
cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Cropped", imgCropped)

cv2.waitKey(0)