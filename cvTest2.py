#!/usr/bin/python

import cv2
import cv
import numpy as np
import time

def body():
	print "opening videoCapture"
	capture = cv2.VideoCapture(0)
	capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
	capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
	capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)

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
	try:
		while flag:
			grey  = cv2.cvtColor(frame, cv.CV_RGB2GRAY)
			edges = cv2.Canny(grey, 0, 100)
			i += 1
			flag, frame = capture.read()
	except KeyboardInterrupt:
		t1 = time.time()
		tt = t1 - t0
	
	print "frames: " + str(i)
	print "time: " + str(tt)
	print "fps: " + str(i/tt)

	print "saving images"
	cv2.imwrite("capture.png", frame)
	cv2.imwrite("edges.png", edges)

if __name__ == "__main__":
	body()

