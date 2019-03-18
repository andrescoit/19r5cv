import cv2

import numpy as np

def canny_webcam():
    "Live capture frames from webcam and show the canny edge image of the captured frames."

    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()  # ret gets a boolean value. True if reading is successful (I think). frame is an
        # uint8 numpy.ndarray

        frame = cv2.GaussianBlur(frame, (7,7), 1.41)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        #Noise removal with iterative bilateral filter(removes noise while preserving edges)
        noise_removal = cv2.bilateralFilter(frame,9,75,75)
        cv2.namedWindow("Noise Removed Image",cv2.WINDOW_NORMAL)
        # Creating a Named window to display image
        cv2.imshow("Noise Removed Image",noise_removal)
        # Display Image

        # Thresholding the image
        ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)
        #cv2.namedWindow("Image after Thresholding",cv2.WINDOW_NORMAL)
        # Creating a Named window to display image
        #cv2.imshow("Image after Thresholding",thresh_image)
        # Display Image


        edge = cv2.Canny(thresh_image, 25, 75)

        #cv2.imshow('Canny Edge', edge)

        #dilation to strengthen edges?
        kernel = np.ones((3,3), np.uint8)
        # Creating the kernel for dilation
        dilated_image = cv2.dilate(edge,kernel,iterations=1)
        #cv2.namedWindow("Dilation", cv2.WINDOW_NORMAL)
        # Creating a Named window to display image
        #cv2.imshow("Dilation", dilated_image)
        
        # Displaying Image
        im2, contours, h = cv2.findContours(dilated_image, 1, 2)
        contours= sorted(contours, key = cv2.contourArea, reverse = True)[:1]
        pt = (180, 3 * edge.shape[0] // 4)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            # print len(cnt)
            print len(approx)
            if len(approx) ==6 :
                print "Cube"
                cv2.drawContours(edge,[cnt],-1,(255,0,0),3)
                cv2.putText(edge,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0,255, 255], 2)
                whatsit = "Cube"
            elif len(approx) == 7:
                print "Cube"
                cv2.drawContours(edge,[cnt],-1,(255,0,0),3)
                cv2.putText(edge,'Cube', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
                whatsit = "Cube"
            elif len(approx) == 8:
                print "Cylinder"
                cv2.drawContours(edge,[cnt],-1,(255,0,0),3)
                cv2.putText(edge,'Cylinder', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [0, 255, 255], 2)
                whatsit = "Cylinder"

            elif len(approx) > 10:
                print "NOTHING"
                cv2.drawContours(edge,[cnt],-1,(255,0,0),3)
                cv2.putText(edge,'NOTHING', pt ,cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, [255, 0, 0], 2)
                whatsit = "NOTHING"
                
        cv2.namedWindow("Shape", cv2.WINDOW_NORMAL)
        cv2.imshow('Shape',edge)

        corners    = cv2.goodFeaturesToTrack(thresh_image,6,0.06,25)
        corners    = np.float32(corners)
        for    item in    corners:
            x,y    = item[0]
            cv2.circle(edge,(x,y),10,255,-1)
        cv2.namedWindow("Corners", cv2.WINDOW_NORMAL)
        cv2.imshow("Corners",edge)


        #test if condition is being stored as variable whatsit
        if  whatsit == 'Cube' :
            print "BOGIE IN SIGHT"
        elif whatsit == 'Cylinder':
            print "GTFA"
        elif whatsit == 'NOTHING':
            print "SHIT NOTHING CAPTAIN"

        
        if cv2.waitKey(20) == ord('q'):  # Introduce 20 milisecond delay. press q to exit.
            break
        
canny_webcam()
