import cv2 
import numpy as np

#img = cv2.imread("/home/whoami/Pictures/cylinder1.jpg")

def get_shape():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 5
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.5) # warmup

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
        ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)
        canny_image = cv2.Canny(thresh_image,250,255)
        kernel = np.ones((3,3), np.uint8)
        dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
        contours, h = cv2.findContours(dilated_image, 1, 2)
        contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
        pt = (180, 3 * img.shape[0] // 4)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            # print len(cnt)
            print len(approx)
            if len(approx) ==6 :
                print "Cube"
                cv2.drawContours(img,[cnt],-1,(255,0,0),3)
                cv2.putText(img,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0,255, 255], 2)
            elif len(approx) == 7:
                print "Cube"
                cv2.drawContours(img,[cnt],-1,(255,0,0),3)
                cv2.putText(img,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
            elif len(approx) == 8:
                print "Cylinder"
                cv2.drawContours(img,[cnt],-1,(255,0,0),3)
                cv2.putText(img,'Cylinder', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
            elif len(approx) > 10:
                print "Sphere"
                cv2.drawContours(img,[cnt],-1,(255,0,0),3)
                cv2.putText(img,'Sphere', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [255, 0, 0], 2)

        cv2.namedWindow("Shape", cv2.WINDOW_NORMAL)
        cv2.imshow('Shape',img)

        corners    = cv2.goodFeaturesToTrack(thresh_image,6,0.06,25)
        corners    = np.float32(corners)
        for    item in    corners:
            x,y    = item[0]
            cv2.circle(img,(x,y),10,255,-1)
        cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
        cv2.imshow("Corners",img)

        rawCapture.truncate(0) # prepare for next frame

        if cv2.waitKey(100) == ord('q'): # quit on 'q' with delay
            break
    return 0
