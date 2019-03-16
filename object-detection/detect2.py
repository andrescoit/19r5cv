import cv2
import numpy as np
import time

def main():
    cap = cv2.VideoCapture(0)
    time.sleep(0.5) # camera warmup

    while True:
        ret, img = cap.read()
        if not ret:
            break
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Noise removal with iterative bilateral filter(removes noise while preserving edges)
        noise_removal = cv2.bilateralFilter(img_gray,9,75,75)

        # Thresholding the image
        ret,thresh_image = cv2.threshold(noise_removal,0,255,cv2.THRESH_OTSU)

        # Applying Canny Edge detection
        canny_image = cv2.Canny(thresh_image,250,255)

        # dilation to strengthen the edges
        kernel = np.ones((3,3), np.uint8)

        # Creating the kernel for dilation
        dilated_image = cv2.dilate(canny_image,kernel,iterations=1)

        # Displaying Image

        #contours, h = cv2.findContours(dilated_image, 1, 2)
        _, contours, h = cv2.findContours(dilated_image, 1, 2)
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

        key = cv2.waitKey(30)
        if key == ord('q') or key == 27:
            break

if __name__ == "__main__":
    main()
