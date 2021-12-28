import  cv2
import numpy as np

img = cv2.imread("Resources/card.jpg")

width,height = 250,350
pts1 = np.float32([[146,105],[219,84],[247,177],[175,199]])
pts2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgoutput = cv2.warpPerspective(img, matrix,(width,height))
cv2.imshow("img",img)
cv2.imshow("imgoutput",imgoutput)
cv2.waitKey(0)