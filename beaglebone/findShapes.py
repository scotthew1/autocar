#!/usr/bin/python

import cv2
import cv
import numpy as np
import time
import argparse

def findShapes( frame ):
	gray = cv2.cvtColor(frame, cv.CV_RGB2GRAY)
	ret, thresh = cv2.threshold( gray, 127, 255, 1 )
	contours, h = cv2.findContours( thresh, 1, 2 )
	
	for cnt in contours:
		approx = cv2.approxPolyDP( cnt, 0.01*cv2.arcLength(cnt,True), True )
		#print len(approx)
		if len(approx) == 3:
			#print "triangle"
			cv2.drawContours( frame, [cnt], 0, (0,255,0), -1 )
		elif len(approx) == 4:
			#print "square"
			cv2.drawContours( frame, [cnt], 0, (0,0,255), -1 )
		elif len(approx) == 8:
			#print "octogon"
			cv2.drawContours( frame, [cnt], 0, (255,255,0), -1 )

def body( args ):
	# open output window if needed
	if args.show:
		cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
	
	print "opening videoCapture"
	if args.infile:
		# cpature from input file
		capture = cv2.VideoCpature( args.infile )
		if not cpature.isOpened():
			print "failed to open video file"
			return
	else:
		# cpature from default camera
		capture = cv2.VideoCapture(0)
		capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
		capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
		capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
		#capture.set(cv.CV_CAP_PROP_FPS, 30)
		if not capture.isOpened():
			print "failed to connect camera"
			return

	print "reading test frame"
	flag, frame = capture.read()

	if not flag:
		print "failed to get frame"
		return

	width = np.size(frame, 1)
	height = np.size(frame, 0)
	print "width: " + str( width )
	print "height: " + str( height )
	
	if args.outfile:
		print "opeing videoWriter"
		f = args.fourcc
		fourcc = cv.CV_FOURCC( f[0], f[1], f[2], f[3] )
		writer = cv2.VideoWriter( args.outfile, fourcc, 20.0, (width,height) )
	
	# time for the loop where all the work gets done
	t0 = time.time()
	i = 0
	try:
		while flag:
			if not args.noprocess:	
				findShapes( frame )
			if args.show:
				cv2.imshow("preview", frame)
				flag, frame = capture.read()
				key = cv2.waitKey(5)
			if args.outfile:
				writer.write( frame )
			i += 1
			flag, frame = capture.read()

	except KeyboardInterrupt:
		pass
	
	t1 = time.time()
	tt = t1 - t0
	
	print "frames: " + str(i)
	print "time: " + str(tt)
	print "fps: " + str(i/tt)

if __name__ == "__main__":	
	parser = argparse.ArgumentParser()
	parser.add_argument( "-i", "--infile", help="use video from an input file rather than the camera" )
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	parser.add_argument( "-s", "--show", help="show the output on screen", action="store_true" )
	parser.add_argument( "-n", "--noprocess", help="disable image processing", action="store_true" )
	args = parser.parse_args()
		
	body( args )

