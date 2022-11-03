import cv2
import numpy as np

img = cv2.imread('/home/pi/Desktop/Smart-Room/iot2/messageImage_1666429018521.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize=3)
lines = cv2.HoughLinesP(edges,1,np.pi/360,100,minLineLength=50,maxLineGap=2)

if lines is not None:
    print("Found Line")
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)

cv2.imshow('Canny edge', edges)
cv2.imshow('houghlinesP', img)
cv2.waitKey(0)
cv2.destroyAllWindows()