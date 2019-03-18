import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vidWrite = cv2.VideoWriter('test_video.avi',fourcc,20,(640,480))


while cap.isOpened():
    ret,frame = cap.read()
    
    vidWrite.write(frame)

    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    cap.release()
    vidWrite.release()
    cv2.destroyAllWindows()
