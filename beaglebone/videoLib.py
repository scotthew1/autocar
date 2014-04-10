#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import cv
import numpy as np
from collections import deque, defaultdict
import logging

Log = logging.getLogger()

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

	def __init__( self, maxLen=5 ):
		self.buffer = deque( maxlen=maxLen )

	def append( self, frame ):
		self.buffer.append( frame )

	def size( self ):
		return len( self.buffer )

	def clear( self ):
		self.buffer.clear()

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

	def printHorzDiff( self ):
		lastFrame = None
		for frame in self.buffer:
			if lastFrame is None:
				lastFrame = frame
			else:
				h1 = lastFrame.horizLines
				h2 = frame.horizLines
				size = min( len(h1), len(h2) )
				diffs = [ h1[i][0] - h2[i][0] for i in range(size) ]
				print diffs


class VideoCapture:
	
	frameCount = 0
	frameBuf = FrameBuffer()
	currentMeta = None
	lastFlowFrame = None
	lastFlowPnts = None

	def __init__( self, infile=None, outfile=None, fourcc="XVID", preview=False ):
		Log.info( "opening videoCapture" )
		if infile:
			# capture from input file
			self.capture = cv2.VideoCapture( args.infile )
			if not self.capture.isOpened():
				raise Exception( "Could not open input file: %s" % infile )
		else:
			# capture from default camera
			Log.info( "connecting to camera" )
			self.capture = cv2.VideoCapture(0)
			self.capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 340)
			self.capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
			# self.capture.set(cv.CV_CAP_PROP_BRIGHTNESS, .5)
			if not self.capture.isOpened():
				raise Exception( "Could not connect to camera." )

		Log.info( "reading test frame" )
		if not self.captureFrame():
			raise Exception( "Could not read from video source." )

		self.width = np.size( self.currentFrame, 1 )
		self.height = np.size( self.currentFrame, 0 )
		Log.info( "width: " + str( self.width ) )
		Log.info( "height: " + str( self.height ) )

		# clear out test frame
		self.frameCount = 0
		self.currentFrame = None

		if outfile:
			Log.info( "opening videoWriter" )
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

	def cleanUp( self ):
		cv2.destroyAllWindows()
		self.capture.release()


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
			# no writer defined
			return
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
		try:
			if slope < 1:
				x1 = 1000
				x2 = -1000
				y1 = int( slope * x1 + yInt )
				y2 = int( slope * x2 + yInt )
			else:
				y1 = 1000
				y2 = -1000
				x1 = int( (y1 - yInt) // slope )
				x2 = int( (y2 - yInt) // slope )
		except ValueError:
			Log.error( "ValueError (slope, yInt): %0.4f, %0.4f" % slope, yInt )
			return

		if frame is not None:
			cv2.line( frame, (x1,y1), (x2,y2), color, 3 )
		elif self.currentFrame is not None:
			cv2.line( self.currentFrame, (x1,y1), (x2,y2), color, 3 )
		else:
			raise Exception( "No frame." )

	def drawHorizontalLine( self, yVal, color, frame=None ):
		if frame is not None:
			cv2.line( frame, (-1000,yVal), (1000,yVal), color, 3 )
		elif self.currentFrame is not None:
			cv2.line( self.currentFrame, (-1000,yVal), (1000,yVal), color, 3 )
		else:
			raise Exception( "No frame." )


	# math functions
	def get2PointSlope( self, line ):
		div = line[2] - line[0]
		if div == 0:
			return 10000
		else:
			return ( line[3] - line[1] ) / float(div)

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
		div   = (sumX2 - sumX * xMean)
		# if div is zero, make slope very large for our purposes
		if div == 0:
			slope = 10000
		else:
			slope = (sumXY - sumX * yMean) / float(div)
		yInt = yMean - slope * xMean
		return slope, yInt

	def getAvgHorizontals( self, horz, drawFrame ):
		"""
		Separates horizontal lines into bins and finds an average
		line for each bin.
		"""
		bins = defaultdict( list )
		for l in horz:
			yAvg = ( l[1] + l[3] ) / 2
			for key in bins:
				if key-20 <= yAvg <= key+20:
					bins[key].append( l )
					break
			else:
				bins[yAvg].append( l )
		out = []
		for key in bins:
			line = self.getBestFit( bins[key] )
			out.append( line )
		return out

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
	def findGaps( self, frame, slope, yInt ):
		if slope == 0:
			Log.error( "zero slope" )
			return False
		lastBit = 1
		out = []
		for y in range( 0, self.height, 4 ):
			x = int( (y - yInt) // slope )
			if x >= self.width:
				continue
			if frame[y][x] != lastBit:
				out.append( (x,y) )
				lastBit = frame[y][x]
		return out

	def checkHorizontal( self, frame, yHorz, slope, yInt ):
		if slope == 0:
			Log.error( "zero slope" )
			return False
		yHorz = int(yHorz)
		y1 = yHorz + 10
		y2 = yHorz - 10
		x1 = int( (y1 - yInt) // slope )
		x2 = int( (y2 - yInt) // slope )
		if y1 >= self.height or y2 < 0 or x1 >= self.width or x2 < 0:
			Log.error( "check points out of range" )
			return [0]
		# get points above and below horz
		above = frame[y1][x1]
		below = frame[y2][x2]
		# find where the line intersects the horz for return
		x = int( (yHorz - yInt) // slope )
		if below and not above:
			Log.debug( "road above horz" )
			return [1, x, yHorz]
		elif above and not below:
			Log.debug( "road below horz" )
			return [2, x, yHorz]
		else:
			return [0]

	def checkPointOnLine( self, frame, slope, yInt, x=None, y=None ):
		"""
		Finds a point on a line given x or y, then checks this point
		and 2 points near it on the frame. 
		Returns the sum of these 3 points or False on error.
		"""
		if not (x or y):
			Log.error( "target x or y must be provided." )
			return False
		elif x and not y:
			y = slope * x + yInt
			if not ( 0 <= x < self.width ) or not ( 2 <= y < self.height-2 ):
				Log.debug( "point is not in frame." )
				return False
			return frame[y][x] | frame[y+2][x] | frame[y-2][x]
		elif y and not x: 
			if not slope:
				Log.error( "slope must be a non-zero number." )
				return false
			x = (y - yInt) / slope
			if not ( 2 <= x < self.width-2 ) or not ( 0 <= y < self.height ):
				Log.debug( "point is not in frame." )
				return False
			return frame[y][x] | frame[y][x+2] | frame[y][x-2]
		else:
			return False

	def findLines( self ):
		if self.currentFrame is None:
			raise Exception( "No frame to process." )

		# these are the output variables
		lineFrame = self.currentFrame.copy()
		avgXIntersect = None
		outHorz = []

		# opencv time, do the filtering and find lines
		gray  = cv2.cvtColor( self.currentFrame, cv.CV_RGB2GRAY )
		ret, thresh = cv2.threshold( gray, 200, 255, cv2.THRESH_BINARY )
		edges = cv2.Canny( thresh, 50, 100 )
		lines = cv2.HoughLinesP( edges, 1, np.pi/180, 30, maxLineGap=10 )
		
		# loop through the lines and separate them 
		if lines is not None:
			( horz, left, right ) = [], [], []
			# loop through all lines found
			midpoint = (self.width/2)
			for l in lines[0]:
				# check the slope to see if the line is horizontal
				slope = self.get2PointSlope( l )
				if slope == 10000:
					# rogue line, we don't care about
					pass
				elif  -0.3 <= slope <= 0.3:
					# mostly horizontal
					horz.append( l )
				elif l[0] < midpoint and l[2] < midpoint and slope <= -1:
					# left side of the screen
					left.append( l )
				elif l[0] > midpoint and l[2] > midpoint and slope >= 1:
					# right side of the screen
					right.append( l )
				else:
					# don't know
					Log.debug( "unknown line: %s" % l )
					Log.debug( "slope: %s" % slope ) 
					cv2.line( lineFrame, (l[0],l[1]), (l[2],l[3]), (0,255,255), 3 )

			lSlope, lYInt = (None, None)
			rSlope, rYInt = (None, None)
			avgXIntersect = self.frameBuf.getAvgXIntersect()
			# find average vertical lines and line intersect
			if len( left ) > 0:
				lSlope, lYInt = self.getBestFit( left )
				self.drawSlopeIntLine( lSlope, lYInt, (0,255,0), lineFrame )
				# gapPnts = self.findGaps( thresh, lSlope, lYInt )
				# for x, y in gapPnts:
				# 	cv2.circle( lineFrame, (x, y), 4, (0,255,255) )
			if len( right ) > 0:
				rSlope, rYInt = self.getBestFit( right )
				self.drawSlopeIntLine( rSlope, rYInt, (255,0,0), lineFrame )
				# gapPnts = self.findGaps( thresh, rSlope, rYInt )
				# for x, y in gapPnts:
				# 	cv2.circle( lineFrame, (x, y), 4, (0,255,255) )
			if lSlope and rSlope:
				x = self.getXIntesectFromSlopeInt( lSlope, lYInt, rSlope, rYInt )
				self.currentMeta.xIntersect = x
				avgXIntersect = self.frameBuf.newAvgXIntersect( x )
			
			# do horizontal line shit
			if len( horz ) > 0:
				ptSlopeHorz = self.getAvgHorizontals( horz, lineFrame )
				ptSlopeHorz.sort(key=lambda tup: tup[1])
				for i in range( len(ptSlopeHorz) ):
					hSlope, hYInt = ptSlopeHorz[i]
					# self.drawHorizontalLine( y, (0,0,255), lineFrame )
					self.drawSlopeIntLine( hSlope, hYInt, (0,0,255), lineFrame )
					if rSlope:
						rtempY = (((ptSlopeHorz[i][1] - ptSlopeHorz[i+1][1])/2) + ptSlopeHorz[i][1])
						rX = (rtempY - rYint) / rSlope
						rightPnt = self.checkPointOnLine( thresh, rSlope, rYint, y=rtempY )
						if rightPnt == False:
							pass
						elif rightPnt == 255:
							cv2.circle(lineFrame, (rX, int(rYint)), 3, (0,0,255), 3 )
						elif rightPnt == 0:
							cv2.circle(lineFrame, (rX, int(rYint)), 3, (0,255,0), 3 )
					if lSlope:
						ltempY = (((ptSlopeHorz[i][1] - ptSlopeHorz[i+1][1])/2) + ptSlopeHorz[i][1])
						lX = (ltempY - lYint) / lSlope
						leftPnt = self.checkPointOnLine( thresh, lSlope, lYint, y=ltempY )
						if leftPnt == False:
							pass
						elif leftPnt == 255:
							cv2.circle(lineFrame, (lX, int(lYint)), 3, (0,0,255), 3 )
						elif leftPnt == 0:
							cv2.circle(lineFrame, (lX, int(lYint)), 3, (0,0,255), 3 )
					# check to see if we can cross the line
					pnt = self.checkPointOnLine( thresh, hSlope, hYInt, x=self.width/2 )
					if pnt == False:
						# an error occurred
						pass
					elif pnt == 255:
						cv2.circle( lineFrame, (self.width/2, int(hYInt)), 3, (0,0,255), 3 )
					elif pnt == 0:
						cv2.circle( lineFrame, (self.width/2, int(hYInt)), 3, (0,255,0), 3 )
					outHorz.append( ( hYInt, pnt ) )


			# draw the midpoint and numeric value
			if avgXIntersect:
				cv2.putText( lineFrame, "x: %d" % avgXIntersect, (10,15), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255) )
				cv2.circle( lineFrame, (avgXIntersect, self.height/2), 4, (0,255,255) )
			
			# save frame metadata
			self.currentMeta.llSlope = lSlope
			self.currentMeta.llYInt  = lYInt
			self.currentMeta.rlSlope = rSlope
			self.currentMeta.rlYInt  = rYInt
			self.currentMeta.horizLines = outHorz
		else:
			Log.info( "no lines detected" )

		return lineFrame, avgXIntersect, outHorz

	def findShapes( self ):
		if self.currentFrame is None:
			raise Exception( "No frame to process." )

		xCount = 0
		# cropping the battery
		img = self.currentFrame
		crop = img[100:200, 100:260]
		# Convert BGR to HSV
		hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
		#define range of GREEN 
		# array( HUE, SATURATION, VALUE/BRIGHTNESS)
		lower_green = np.array([45,85,65])
		upper_green = np.array([70,255,255])
		#define range of RED - Kyle
		lower_red = np.array([170,50,50])
		upper_red = np.array([10,255,255])
		#define range of BLUE
		lower_blue = np.array([100,40,40])
		upper_blue = np.array([130,255,255])
		#Using greenmask to find everything within a range of the given values
		#and returning this to help find signs on the road
		greenmask = cv2.inRange(hsv, lower_green, upper_green)
		redmask = cv2.inRange(hsv, lower_red, upper_red)
		bluemask = cv2.inRange(hsv, lower_blue, upper_blue)
		# edges = cv2.Canny( greenmask, 50, 100 )
		# Checks to see if we see enough green for there to be an arrow in the image
		# Counts the number of non-zero values in the array 
		greencount = np.count_nonzero(greenmask)
		redcount = np.count_nonzero(redmask)
		bluecount = np.count_nonzero(bluemask)
		if redcount >= 400 and redcount < 3000:
			Log.info( "Stop Sign detected" )
			direction = 'StopSign'
		elif bluecount >= 1200:
			#destination has been reached
			# stop function
			# LED light show?
			Log.info("Destination detected")
			direction = 'Destination'
		elif greencount >= 1100:
			# Log.debug( "%s" % greencount )
			# convert to grayscale
			gray = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
			corners = cv2.goodFeaturesToTrack(gray,7,0.01,10)
			corners = np.int0(corners)
			# Log.debug( "I see an arrow" )
			#find max and min x & y values
			xCoor = list()
			yCoor = list()
			for i in range(len(corners)):
				xCoor.append(int(corners[i][0][0]))
				yCoor.append(int(corners[i][0][1]))
			yCoorSorted = sorted(yCoor)
			xCoorSorted = sorted(xCoor)
			# Log.debug( "xCoor: " + str(xCoor) )
			#find length of list, then find value of 0
			# and max index then subtract to find length
			yMaxIndex = (len(yCoorSorted) - 1)
			xMaxIndex = (len(xCoorSorted) - 1)
			yValue = yCoorSorted[yMaxIndex] - yCoorSorted[0]
			xValue = xCoorSorted[xMaxIndex] - xCoorSorted[0]
			halfxVal = xValue/2
			testTip = (halfxVal + xCoorSorted[0])

			# Log.debug( "testTip: " + str(testTip) )
			for j in range(len(xCoor)):
				if ((xCoorSorted[xMaxIndex] - xCoorSorted[xMaxIndex-1]) <= 5):
					Log.info( "Left Arrow" )
					direction = 'Left'
				elif((xCoorSorted[1] - xCoorSorted[0]) <= 5):
					Log.info( "Right Arrow" )
					direction = 'Right'
				elif ((testTip > xCoorSorted[j]) and (testTip < xCoorSorted[j+1])):
					xValue = xCoorSorted[j+1]
					# Log.debug( "xValue: " + str(xValue) )
					for k in range(len(xCoor)):
						if xValue == xCoor[k]:
							vertTip = yCoor[k]
							# Log.debug( "vertTip: " + str(vertTip) )
							# Log.debug( "yCoor: " + str(yCoor) )
							if ((vertTip == yCoorSorted[yMaxIndex]) or ((yCoorSorted[1] - yCoorSorted[0]) <= 5)):
									Log.info( "Down Arrow" )
									direction = 'Down'
							elif ((vertTip == yCoorSorted[0]) or ((yCoorSorted[yMaxIndex] - yCoorSorted[yMaxIndex-1]) <= 5)):
									Log.info( "Up Arrow" )
									direction = 'Up'
			#num = 0
			#if num < 1:
			#	cv2.imwrite("thumbnail.jpg", img)
			# for i in corners:
			# 	x,y = i.ravel()
			# 	cv2.circle(gray,(x,y),3,255,-1)

		return direction

	def trackCorners( self ):
		"""
		with help from:
		http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html 
		"""
		if self.currentFrame is None:
			raise Exception( "No frame to process." )

		gray  = cv2.cvtColor( self.currentFrame, cv.CV_RGB2GRAY )
		ret, thresh = cv2.threshold( gray, 200, 255, cv2.THRESH_BINARY )

		if self.lastFlowPnts is None:
			feature_params = dict( maxCorners = 100,
							qualityLevel = 0.3,
							minDistance = 7,
							blockSize = 7 )
			p0 = cv2.goodFeaturesToTrack( thresh, mask=None, **feature_params )

		# Select good points
		good_new = p1[st==1]
		good_old = p0[st==1]


if __name__ == "__main__":
	import sys
	import traceback
	from time import time, sleep
	from argparse import ArgumentParser


	parser = ArgumentParser()
	parser.add_argument( "-v", "--verbose", help="log debug data", action="store_true" )
	parser.add_argument( "--logfile", help="specify a file to log to rather than the console" )
	parser.add_argument( "-i", "--infile", help="use video from an input file rather than the camera" )
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "-f", "--function", help="choose image processing function, current options are 'none', 'lines', 'shapes', 'corners'", default='none' )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	parser.add_argument( "-s", "--show", help="show the output on screen", action="store_true" )
	parser.add_argument( "-l", "--framelimit", type=int, help="number of frames to capture" )
	args = parser.parse_args()

	kwargs = {}
	if args.verbose:
		kwargs['level'] = logging.DEBUG
	else:
		kwargs['level'] = logging.INFO
	if args.logfile:
		kwargs['filename'] = args.logfile
	kwargs['format'] = '%(levelname)s %(module)s.%(funcName)s: %(message)s'
	kwargs['datefmt'] = '%H:%M:%S'
	
	logging.basicConfig( **kwargs )

	# log uncaught exceptions
	# thanks http://stackoverflow.com/a/8054179
	def logException( type, value, tb ):
		Log.exception( "Uncaught exception: {0}".format( str(value) ) )
	
	sys.excepthook = logException

	if args.function not in [ 'none', 'lines', 'shapes', 'corners' ]:
		Log.error( "The function you specified is not supported." )
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
				lineFrame, intersect, horz = vc.findLines()
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
			elif args.function == 'corners':
				cornerFrame = vc.findShapes()
				vc.drawGrid( cornerFrame )
				if args.outfile:
					vc.writeFrame( cornerFrame )
				if args.show:
					vc.previewFrame( cornerFrame )
					# sleep( 0.03 )
			vc.saveFrameToBuf()
			if args.framelimit and vc.frameCount >= args.framelimit:
				break
	except KeyboardInterrupt:
		pass

	t1 = time()
	tt = t1 - t0
	
	Log.info( "frames: %d" % vc.frameCount )
	Log.info( "time: %f" % tt )
	Log.info( "fps: %f" % (vc.frameCount/tt) )

	vc.cleanUp()
