import cv2
import numpy as np
#WebCam!!! and we can develop it!!
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)#brightness

myColors =[[5,107,0,19,255,255],
           [133,56,0,159,156,255],
           [57,76,0,100,255,255]]

e
def findColor(img,myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[2][0:3])
    upper = np.array(myColors[2][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("img",mask)


while True:
    success, img = cap.read()
    findColor(img, myColors)
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break