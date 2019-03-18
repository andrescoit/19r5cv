import io
import picamera
import cv2
import numpy as np

stream = io.BytesIO()

with picamera.PiCamera() as camera: camera.resolution = (640, 480), camera.capture(stream, format='jpeg')

buff = numpy.fromstring(Stream.getvalue(), dtype=numpy.uint8)

image = cv2.imdecode(buff, 1)

cube_cascade = cv2.CascadeClassifier('/home/pi/data/cube1-cascade-10stages.xml')

gray = cv2.cvtColor(image, cv.COLOR_BGR2GRAY)

Cube = cube_cascade.detectMultiScale(gray, 1.1, 5)

print "Found "+str(len(Cube))+" cube(s)"

for (x,y,w,h) in Cube: cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,0), 2)

cv2.imwrite('result.jpg', image)


