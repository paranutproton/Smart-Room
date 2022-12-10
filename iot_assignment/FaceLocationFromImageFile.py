import face_recognition
import cv2

FileLocation = "/home/pi/Desktop/Smart-Room/iot2/S__27099169.jpg"

img = face_recognition.load_image_file(FileLocation)
face_location = face_recognition.face_locations(img)
print(face_location)
print("There are " + str(len(face_location)) + " people in this image.")

# ROI to opencv format location
x0 = face_location[0][3] # Left
y0 = face_location[0][0] # Top
x1 = face_location[0][1] # Bottom
y1 = face_location[0][2] # Right

img2 = cv2.imread(FileLocation)
cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Resized_Window", 400, 400)
cv2.rectangle(img2,(x0,y0),(x1,y1),(255,0,0),3)
cv2.imshow("Resized_Window",img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

