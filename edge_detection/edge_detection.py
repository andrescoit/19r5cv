from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils

#width = 800

def canny_webcam():
    "Live capture frames from webcam and show the canny edge image of the captured frames."

    # cap = cv2.VideoCapture(0)
    camera = cv2.VideoCapture(0)
    time.sleep(0.5) # allow comera warmup

    while True:
        #ret, frame = cap.read()  # ret gets a boolean value. True if reading is successful (I think). frame is an
        (ret, frame) = camera.read()
        # uint8 numpy.ndarray

        #frame = imutils.resize(frame, width=width)

        #frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if ret is True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            break
        gray = cv2.GaussianBlur(gray, (7,7), 1.41)

        #edge = cv2.Canny(frame, 25, 75)
        edge = cv2.Canny(gray, 25, 75)
 
        cv2.imshow('Canny Edge', edge)

        if cv2.waitKey(20) == ord('q'):  # Introduce 20 milisecond delay. press q to exit.
            break

canny_webcam()
