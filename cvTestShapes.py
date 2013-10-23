#!/usr/bin/python

import cv2
import cv
import numpy as np
import time

cannyVal = 30

# def nullFunc(val):
#	global cannyVal
#	cannyVal = val
#	return

def body():
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

	try:
		while flag:
			gray = cv2.cvtColor(frame, cv.CV_RGB2GRAY)
			ret, thresh = cv2.threshold(gray, 127, 255, 1)
			contours, h = cv2.findContours(thresh,1,2)
			
			for cnt in contours:
				approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True), True)
				# print len(approx)
				if len(approx) == 3:
					print "triangle"
					cv2.drawContours(frame, [cnt], 0, (0,255,0), -1)
				elif len(approx) == 4:
					print "square"
					cv2.drawContours(frame, [cnt], 0, (0,0,255), -1)
				elif len(approx) == 8:
					print "octogon"
					cv2.drawContours(frame, [cnt], 0, (255,255,0), -1)
	
			i += 1
			flag, frame = capture.read()
	except KeyboardInterrupt:	
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

