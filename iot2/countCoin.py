import cv2
import numpy as np

img = cv2.imread('/home/pi/Desktop/Smart-Room/iot2/S__25223190.jpg') #dont forget to change path file
cv2.imshow('original image', img)
blur = cv2.medianBlur(img, 5)

dimensions = img.shape

gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1.2, dimensions[0]/20)

thickness = 2

count = 0

if circles is not None:
    print("Found circle")
    circles = np.uint16(circles[0, :])
    print(circles)
    for( x,y, diameter) in circles :
        cv2.circle(img,(x,y), diameter, (0,0,255), thickness, cv2.LINE_AA)
        cv2.circle(img, (x,y), 2,(0,255,0), thickness)
        count += 1
else:
    print("Connot detect circle.")

print("Number of coin(s): ",count)
# Allows us to see image
# until closed forcefully
cv2.imshow('Detected circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()