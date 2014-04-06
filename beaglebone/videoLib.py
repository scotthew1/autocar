#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import cv
import numpy as np
from collections import deque


class FrameMeta:

	llSlope = None
	llYInt  = None
	rlSlope = None
	rlYInt  = None
	horizLines = None
	xIntersect = None

	def __init__( self, image ):
		self.img = image


class FrameBuffer:

	def __init__( self, maxLen=10 ):
		self.buffer = deque( maxlen=maxLen )

	def append( self, frame ):
		self.buffer.append( frame )

	def size( self ):
		return len( self.buffer )

	def getAvgXIntersect( self ):
		intersects = [ frame.xIntersect for frame in self.buffer if frame.xIntersect ]
		if len( intersects ) > 0:
			return sum( intersects ) / len( intersects )
		else:
			return None

	def newAvgXIntersect( self, x ):
		intersects = [ frame.xIntersect for frame in self.buffer if frame.xIntersect ]
		if len( intersects ) > 0:
			intersects.append( x )
			return sum( intersects ) / len( intersects )
		else:
			return x


class VideoCapture:
	
	frameCount = 0
	frameBuf = FrameBuffer()
	currentMeta = None

	def __init__( self, infile=None, outfile=None, fourcc="XVID", preview=False ):
		print "opening videoCapture"
		if infile:
			# capture from input file
			self.capture = cv2.VideoCapture( args.infile )
			if not self.capture.isOpened():
				raise Exception( "Could not open input file: %s" % infile )
		else:
			# capture from default camera
			print "connecting to camera"
			self.capture = cv2.VideoCapture(0)
			self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
			self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
			# self.capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
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


	# capturing / storing frames
	def captureFrame( self ):
		flag, self.currentFrame = self.capture.read()
		self.currentMeta = FrameMeta( self.currentFrame )
		if flag:
			self.frameCount += 1
		return flag

	def saveFrameToBuf( self, frame=None ):
		if frame is not None:
			self.frameBuf.append( frame )
		else:
			self.frameBuf.append( self.currentMeta )

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


	# drawing functions
	def drawGrid( self, frame=None ):
		color = (0,0,0)
		thick = 1
		vert1 = self.width / 4
		vert2 = self.width / 2
		vert3 = 3 * ( self.width / 4 )
		horz1 = self.height / 4
		horz2 = self.height / 2
		horz3 = 3 * ( self.height / 4 )

		if frame is not None:
			cv2.line( frame, (vert1,-1000), (vert1,1000), color, thick )
			cv2.line( frame, (vert2,-1000), (vert2,1000), color, thick )
			cv2.line( frame, (vert3,-1000), (vert3,1000), color, thick )
			cv2.line( frame, (-1000,horz1), (1000,horz1), color, thick )
			cv2.line( frame, (-1000,horz2), (1000,horz2), color, thick )
			cv2.line( frame, (-1000,horz3), (1000,horz3), color, thick )
		elif self.currentFrame is not None:
			cv2.line( self.currentFrame, (vert1,-1000), (vert1,1000), color, thick )
			cv2.line( self.currentFrame, (vert2,-1000), (vert2,1000), color, thick )
			cv2.line( self.currentFrame, (vert3,-1000), (vert3,1000), color, thick )
			cv2.line( self.currentFrame, (-1000,horz1), (1000,horz1), color, thick )
			cv2.line( self.currentFrame, (-1000,horz2), (1000,horz2), color, thick )
			cv2.line( self.currentFrame, (-1000,horz3), (1000,horz3), color, thick )
		else:
			raise Exception( "No frame." )

	def drawSlopeIntLine( self, slope, yInt, color, frame=None ):
		"""
		y = slope * x + yInt
		x = (y - yInt) / slope
		"""
		y1 = 1000
		y2 = -1000
		x1 = int( (y1 - yInt) / slope )
		x2 = int( (y2 - yInt) / slope )

		if frame is not None:
			cv2.line( frame, (x1,y1), (x2,y2), color, 3 )
		elif currentFrame is not None:
			cv2.line( self.currentFrame, (x1,y1), (x2,y2), color, 3 )
		else:
			raise Exception( "No frame." )


	# math functions
	def getBestFit( self, lines ):
		"""
		Finds a best fit line from a list of lines
		With help from http://faculty.cs.niu.edu/~hutchins/csci230/best-fit.htm
		x1 = l[0]; y1 = l[1]; x2 = l[2]; y2 = l[3]
		"""
		points = []
		count, sumX, sumY, sumX2, sumXY = ( 0, 0, 0, 0, 0 )
		for l in lines:
			points.append( (l[0], l[1]) )
			points.append( (l[2], l[3]) )
			count += 2
			sumX  += l[0] + l[2]
			sumY  += l[1] + l[3]
			sumX2 += l[0]*l[0] + l[2]*l[2]
			sumXY += l[0]*l[1] + l[2]*l[3]
		xMean = sumX / float(count)
		yMean = sumY / float(count)
		slope = (sumXY - sumX * yMean) / (sumX2 - sumX * xMean)
		yInt = yMean - slope * xMean
		return slope, yInt

	def getAvgLine( self, lines ):
		outLine = [0, 0, 0, 0]
		length  = len( lines )
		for l in lines:
			outLine[0] += l[0]
			outLine[1] += l[1]
			outLine[2] += l[2]
			outLine[3] += l[3]
		outLine[0] = outLine[0] / length
		outLine[1] = outLine[1] / length
		outLine[2] = outLine[2] / length
		outLine[3] = outLine[3] / length
		return outLine

	def getXIntersectFromSegs( self, l1, l2 ):
		"""
		Finds an x intersect based on 2 line segments
		With help from http://en.wikipedia.org/wiki/Line–line_intersection
		x1 = l1[0]; y1 = l1[1]; x2 = l1[2]; y2 = l1[3]
		x3 = l2[0]; y3 = l2[1]; x4 = l2[2]; y4 = l2[3]

		(x1*y2 - y1*x2)(x3-x4) - (x1-x2)(x3*y4 - y3*x4)
		-----------------------------------------------
		         (x1-x2)(y3-y4)-(y1-y2)(x3-x4)
		"""
		x = ( (l1[0]*l1[3] - l1[1]*l1[2])*(l2[0]-l2[2]) - (l1[0]-l1[2])*(l2[0]*l2[3] - l2[1]*l2[2]) ) / ( (l1[0]-l1[2])*(l2[1]-l2[3])-(l1[1]-l1[3])*(l2[0]-l2[2]) )
		return x

	def getXIntesectFromSlopeInt( self, s1, i1, s2, i2 ):
		"""
		Finds an x intersect based on 2 lines in slope-intersect form
		With help from http://en.wikipedia.org/wiki/Line–line_intersection
		line1: y = s1*x + i1; line2: y = s2*x + i2
		"""
		x = int( ( i2 - i1 ) / ( s1 - s2 ) )
		return x

	# image processing functions
	def findLines( self ):
		if self.currentFrame is None:
			raise Exception( "No frame to process." )
		gray  = cv2.cvtColor( self.currentFrame, cv.CV_RGB2GRAY )
		ret, thresh = cv2.threshold( gray, 230, 255, cv2.THRESH_BINARY )
		edges = cv2.Canny( thresh, 50, 100 )
		lines = cv2.HoughLinesP( edges, 1, np.pi/180, 60, maxLineGap=10 )
		lineFrame = self.currentFrame.copy()
		avgXIntersect = None
		if lines is not None:
			( horz, left, right ) = [], [], []
			# loop through all lines found
			midpoint = (self.width/2)
			for l in lines[0]:
				# x1 = l[0]; y1 = l[1]; x2 = l[2]; y2 = l[3]
				yRatio = l[1] / float(l[3])
				if .8 <= yRatio <= 1.2:
					# mostly horizontal
					cv2.line( lineFrame, (l[0],l[1]), (l[2],l[3]), (0,0,255), 3 )
					horz.append( l )
				elif l[0] < midpoint:
				# elif l[0] < midpoint and l[2] < midpoint:
					# left side of the screen
					left.append( l )
				elif l[0] > midpoint:
				# elif l[0] > midpoint and l[2] > midpoint:
					# right side of the screen
					right.append( l )
				else:
					# don't know
					cv2.line( lineFrame, (l[0],l[1]), (l[2],l[3]), (0,255,255), 3 )

			lSlope, lYInt = (None, None)
			rSlope, rYInt = (None, None)
			avgXIntersect = self.frameBuf.getAvgXIntersect()
			# find average lines and line intersect
			if len( left ) > 0:
				lSlope, lYInt = self.getBestFit( left )
				self.drawSlopeIntLine( lSlope, lYInt, (0,255,0), lineFrame )
			if len( right ) > 0:
				rSlope, rYInt = self.getBestFit( right )
				self.drawSlopeIntLine( rSlope, rYInt, (255,0,0), lineFrame )
			if lSlope and rSlope:
				x = self.getXIntesectFromSlopeInt( lSlope, lYInt, rSlope, rYInt )
				self.currentMeta.xIntersect = x
				avgXIntersect = self.frameBuf.newAvgXIntersect( x )
				cv2.putText( lineFrame, "x: %d" % avgXIntersect, (10,15), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255) )
				cv2.circle( lineFrame, (avgXIntersect, self.height/2), 4, (0,255,255) )
			elif avgXIntersect is not None:
				cv2.putText( lineFrame, "x: %d" % avgXIntersect, (10,15), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255) )
				cv2.circle( lineFrame, (avgXIntersect, self.height/2), 4, (0,255,255) )
			self.currentMeta.llSlope = lSlope
			self.currentMeta.llYInt  = lYInt
			self.currentMeta.rlSlope = rSlope
			self.currentMeta.rlYInt  = rYInt
			self.currentMeta.horizLines = horz
		else:
			print "no lines detected"

		return lineFrame, avgXIntersect


	# TODO: put into a working state
	def findShapes( self ):

		# Convert BGR to HSV
		self.hsv = cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2HSV)

		#gray = cv2.cvtColor(self.currentFrame, cv.CV_RGB2GRAY)

		#define range of yellow
		#lower_green = np.array([50,50,50])
		#upper_green = np.array([70,255,255])

		#define range of Green - Kyle
		# array( HUE, SATURATION, VALUE/BRIGHTNESS)
		lower_green = np.array([45,85,65])
		upper_green = np.array([70,255,255])

		#Using greenmask to find everything within a range of green values
		#and returning this to help find signs on the road
		greenmask = cv2.inRange(self.hsv, lower_green, upper_green)

		#ret, thresh = cv2.threshold( gray, 127, 255, 1 )
		#contours, h = cv2.findContours( thresh, 1, 2 )

		#avgContors = 0
		
		#print "there are " + str(len(contours)) + " contours."
		# update contour average
		#avgContors = ( len(contours) + self.frameCount*avgContors ) / (self.frameCount + 1)

		#for cnt in contours:
			#print "contour"
			#print cnt
			#approx = cv2.approxPolyDP( cnt, 0.01*cv2.arcLength(cnt,True), True )
			#approx = len(cnt)
			#print "approx"
			#print approx
			#if len(approx) != len(cnt):
				#print "len(cnt) = " + str(len(cnt)) + ", len(approx) = " + str(len(approx))
			
			#if len(approx) == 3:
			 	#print "triangle"
			 	#cv2.drawContours( frame, [cnt], 0, (0,255,0), -1 )
			#elif len(approx) == 4:
			 	#print "square"
			 	#cv2.drawContours( frame, [cnt], 0, (0,0,255), -1 )
			#elif len(approx) == 8:
			 	#print "octagon"
			 	#cv2.drawContours( frame, [cnt], 0, (255,255,0), -1 )

		return greenmask


if __name__ == "__main__":
	from time import time, sleep
	from argparse import ArgumentParser
	import sys

	parser = ArgumentParser()
	parser.add_argument( "-i", "--infile", help="use video from an input file rather than the camera" )
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "-f", "--function", help="choose image processing function, current options are 'none', 'lines', 'shapes'", default='none' )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	parser.add_argument( "-s", "--show", help="show the output on screen", action="store_true" )
	parser.add_argument( "-l", "--framelimit", type=int, help="number of frames to capture" )
	args = parser.parse_args()

	if args.function not in [ 'none', 'lines', 'shapes' ]:
		print "The function you specified is not supported."
		parser.print_help()
		sys.exit(0)

	vc = VideoCapture( infile=args.infile, outfile=args.outfile, fourcc=args.fourcc, preview=args.show )

	t0 = time()
	try:
		while vc.captureFrame():
			if args.function == 'none':
				if args.outfile:
					vc.writeFrame()
				if args.show:
					vc.previewFrame()
					# sleep( 0.03 )
			elif args.function == 'lines':	
				lineFrame, intersect = vc.findLines()
				vc.drawGrid( lineFrame )
				if args.outfile:
					vc.writeFrame( lineFrame )
				if args.show:
					vc.previewFrame( lineFrame )
					# sleep( 0.03 )
			elif args.function == 'shapes':
				shapeFrame = vc.findShapes()
				vc.drawGrid( shapeFrame )
				if args.outfile:
					vc.writeFrame( shapeFrame )
				if args.show:
					vc.previewFrame( shapeFrame )
					# sleep( 0.03 )
			vc.saveFrameToBuf()
			if args.framelimit and vc.frameCount >= args.framelimit:
				break
	except KeyboardInterrupt:
		pass

	t1 = time()
	tt = t1 - t0
	
	print "frames: %d" % vc.frameCount
	print "time: %f" % tt
	print "fps: %f" % (vc.frameCount/tt)

