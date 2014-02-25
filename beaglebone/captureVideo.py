#!/usr/bin/python

import cv2
import cv
import numpy as np
import time
import argparse
import pprint

def body( args ):
	print "opening videoCapture"
	capture = cv2.VideoCapture(0)
	capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
	capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
	#capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
	#capture.set(cv.CV_CAP_PROP_FPS, 30)

	if not capture.isOpened():
		print "failed to connect camera"
		return

	print "testing read"
	flag, frame = capture.read()

	if not flag:
		print "failed to get frame"
		return

	width = np.size( frame, 1 )
	height = np.size( frame, 0 )
	print "width: " + str( width )
	print "height: " + str( height )
	
	print "opening videoWriter"
	f = args.fourcc
	fourcc = cv.CV_FOURCC( f[0], f[1], f[2], f[3] )
	writer = cv2.VideoWriter( args.filename, fourcc, 20.0, (width,height) )

	t0 = time.time()
	i = 0
	
	try:
		while flag:
			writer.write(frame)
			flag, frame = capture.read()
			i += 1;
			if i > 300:
				break
	except KeyboardInterrupt:
		pass	
	
	t1 = time.time()
	tt = t1 - t0
	
	print "frames: " + str(i)
	print "time: " + str(tt)
	print "fps: " + str(i/tt)

	capture.release()
	writer.release()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument( "filename", help="the name of the output file" )
	parser.add_argument( "--fourcc", help="the four character code for video output type", default="XVID" )
	args = parser.parse_args()
	
	body( args )

