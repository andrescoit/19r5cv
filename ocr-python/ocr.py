import cv2
import numpy as np
import pytesseract
from PIL import Image
import sys
import os.path
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# usage:
# $python ocr.py [filename.jpg]

#input_file = sys.argv[1]


#def get_string(img_path):
def get_string():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 5
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    # Read image with opencv
    #img = cv2.imread(img_path)
    
    time.sleep(0.5)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        # https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
        # --psm 10 "Treat the image as a single character."
        # --oem  2 "Legacy + LSTM engines"
        tessdata_dir_config = '--tessdata-dir "/usr/share/tesseract-ocr/tessdata" --psm 10 --oem 2 -c tessedit_char_whitelist=ABCDEFG'

        # Write image after removed noise
        #cv2.imwrite("removed_noise.png", img)

        # Apply threshold to get image with only black and white
        #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # Write the image after apply opencv to do some ...
        #cv2.imwrite(img_path, img)

        # Prepare for next frame
        rawCapture.truncate(0)

        # Recognize text with tesseract for python
        #result = pytesseract.image_to_string(Image.open(img_path))
        result = pytesseract.image_to_string(img, config = tessdata_dir_config)
        print result
        print "\n"

        # Show corresponding image
        cv2.imshow('OCR View', img) 
        if cv2.waitKey(200) == ord('q'):
            break

    return 0
    #return result


# Remove in final version
# Instead call get_string function from another file
#print(get_string(input_file))
get_string()




