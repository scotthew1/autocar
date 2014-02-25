#!/usr/bin/python

import cv2
import cv
import numpy as np
import time

cannyVal = 30

def nullFunc(val):
	global cannyVal
	cannyVal = val
	return

def body():
	cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
	value = 30
	cv.CreateTrackbar("tracker", "preview", value, 100, nullFunc)
	print "opening videoCapture"
	capture = cv2.VideoCapture(0)
	capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
	capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
	capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
	#capture.set(cv.CV_CAP_PROP_FPS, 30)

	if not capture.isOpened():
		print "failed to connect camera"
		return

	print "reading frame"
	flag, frame = capture.read()

	if not flag:
		print "failed to get frame"
		return

	print "width: " + str(np.size(frame, 1))
	print "height: " + str(np.size(frame, 0))
	
	t0 = time.time()
	i = 0
	
	while flag:
		edges = cv2.cvtColor(frame, cv.CV_RGB2GRAY)
		frame = cv2.Canny(edges, 0, cannyVal)
		cv2.imshow("preview", frame)
		print "cannyVal is: " + str(cannyVal)
		#print "frame: " + str(i)
		i += 1
		cv2.imshow("preview", frame)
		flag, frame = capture.read()
		key = cv2.waitKey(5)
		if key == 27: # exit on ESC
			break
	
	t1 = time.time()
	tt = t1 - t0
	
	print "frames: " + str(i)
	print "time: " + str(tt)
	print "fps: " + str(i/tt)

	#print "saving images"
	#cv2.imwrite("capture.png", frame)
	#cv2.imwrite("edges.png", edges)

if __name__ == "__main__":
	body()

