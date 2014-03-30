#!/usr/bin/python

import cv2
import cv
import numpy as np
import time
import argparse

class VideoCapture:
	frameCount = 0

	def __init__( self, infile=None, outfile=None, fourcc="XVID", preview=False ):
		print "opening videoCapture"
		if infile:
			# capture from input file
			self.capture = cv2.VideoCpature( args.infile )
			if not self.capture.isOpened():
				raise Exception( "Could not open input file: %s" % infile )
		else:
			# capture from default camera
			self.capture = cv2.VideoCapture(0)
			self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
			self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
			self.capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
			if not self.capture.isOpened():
				raise Exception( "Could not connect to camera." )

		print "reading test frame"
		if not self.captureFrame():
			raise Exception( "Could not read from video source." )

		self.width = np.size( self.currentFrame, 1 )
		self.height = np.size( self.currentFrame, 0 )
		print "width: " + str( self.width )
		print "height: " + str( self.height )

		# clear out test frame
		self.frameCount = 0
		self.currentFrame = None

		if outfile:
			print "opening videoWriter"
			f = fourcc
			fourcc = cv.CV_FOURCC( f[0], f[1], f[2], f[3] )
			self.writer = cv2.VideoWriter( outfile, fourcc, 20.0, (self.width,self.height) )
		else:
			self.writer = None

		if preview:
			cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
			self.preview = True
		else:
			self.preview = False

	def captureFrame( self ):
		flag, self.currentFrame = self.capture.read()
		if flag:
			self.frameCount += 1
		return flag

	def writeFrame( self, frame=None ):
		if not self.writer:
			raise Exception( "Cannot write frame; no writer defined." )
		if frame is not None:
			self.writer.write( frame )
		elif self.currentFrame is not None:
			self.writer.write( self.currentFrame )
		else:
			raise Exception( "No frame to write." )

	def previewFrame( self, frame=None ):
		if not self.preview:
			raise Exception( "Cannot preview frame; preview not enabled." )
		if frame is not None:
			cv2.imshow( "preview", frame )
			key = cv2.waitKey(5)
		elif self.currentFrame is not None:
			cv2.imshow( "preview", self.currentFrame )
			key = cv2.waitKey(5)
		else:
			raise Exception( "No frame to preview." )

	def findLines( self ):
		if self.currentFrame is None:
			raise Exception( "No frame to process." )
		edges = cv2.Canny( self.currentFrame, 50, 200 )
		gray  = cv2.cvtColor( edges, cv.CV_RGB2GRAY )
		lines = cv2.HoughLinesP( gray, 1, cv.CV_PI/180, 50 )
		for line in lines:
			print line

	def findShapes( self ):
		# global frameCount, avgContors

		gray = cv2.cvtColor( self.currentFrame, cv.CV_RGB2GRAY )
		ret, thresh = cv2.threshold( gray, 127, 255, 1 )
		contours, h = cv2.findContours( thresh, 1, 2 )
		
		print "there are " + str(len(contours)) + " contours."
		# update contour average
		avgContors = ( len(contours) + frameCount*avgContors ) / (frameCount + 1)

		for cnt in contours:
			# print "contour"
			# print cnt
			approx = cv2.approxPolyDP( cnt, 0.01*cv2.arcLength(cnt,True), True )
			# approx = len(cnt)
			# print "approx"
			# print approx
			if len(approx) != len(cnt):
				print "len(cnt) = " + str(len(cnt)) + ", len(approx) = " + str(len(approx))
			
			# if len(approx) == 3:
			# 	#print "triangle"
			# 	cv2.drawContours( frame, [cnt], 0, (0,255,0), -1 )
			# elif len(approx) == 4:
			# 	#print "square"
			# 	cv2.drawContours( frame, [cnt], 0, (0,0,255), -1 )
			# elif len(approx) == 8:
			# 	#print "octagon"
			# 	cv2.drawContours( frame, [cnt], 0, (255,255,0), -1 )


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument( "-i", "--infile", help="use video from an input file rather than the camera" )
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	parser.add_argument( "-s", "--show", help="show the output on screen", action="store_true" )
	parser.add_argument( "-n", "--noprocess", help="disable image processing", action="store_true" )
	parser.add_argument( "-l", "--framelimit", type=int, help="number of frames to capture", default=100 )
	args = parser.parse_args()

	print args

	vc = VideoCapture( infile=args.infile, outfile=args.outfile, fourcc=args.fourcc, preview=args.show )

	t0 = time.time()
	while vc.captureFrame() and vc.frameCount < args.framelimit:
		vc.findLines()
		if args.outfile:
			vc.writeFrame()
		if args.show:
			vc.previewFrame()

	t1 = time.time()
	tt = t1 - t0
	
	print "frames: %d" % vc.frameCount
	print "time: %f" % tt
	print "fps: %f" % (vc.frameCount/tt)

