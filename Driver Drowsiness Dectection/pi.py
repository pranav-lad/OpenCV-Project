from scipy.spatial import distance
import dlib
import cv2
from imutils import face_utils
import imutils
import pygame

def eye_aspect_ratio(eye):
    a = distance.euclidean(eye[1], eye[5])
    b= distance.euclidean(eye[2], eye[4])
    c= distance.euclidean(eye[0], eye[3])
    ear = (a + b) / (2.0 * c)
    return ear

pygame.mixer.init()
pygame.mixer.music.load('Resources/Jump1 (1).wav')#-----------------------------------------------------------

thresh = 0.25
frame_check = 20
count = 0
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor(".\shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=900)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)
    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        leftEyeAspectRatio = eye_aspect_ratio(leftEye)
        rightEyeAspectRatio = eye_aspect_ratio(rightEye)
        EyeaspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if (EyeaspectRatio < thresh):
            count += 1

            if count >= frame_check:
                pygame.mixer.music.play(-1)#-----------------------------------------------------------
                cv2.putText(frame, "  Driver is Drowsy ", (150,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
        else:
            pygame.mixer.music.stop()
            count = 0
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
     break
cv2.destroyAllWindows()
cap.stop()
