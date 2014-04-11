#!/usr/bin/python

from bbio import *
from cv2 import circle
from videoLib import VideoCapture
import commandLib as cl
import random
import logging

Log = logging.getLogger()

global vc
nextTurn = 'Left'

def forwardMovement():
	global nextTurn

	lastNudge = 0
	intersect = None
	while vc.captureFrame():
		lineFrame, intersect, horz = vc.findLines()
		if vc.checkReset():
			Log.info( "resetting...." )
			return False
		# vc.frameBuf.printHorzDiff()
		# if nextTurn == None:
		# next = vc.findShapes()
		cornerFrame = vc.trackCorners()
		
		vc.drawGrid( cornerFrame )
		vc.writeFrame( cornerFrame )
		vc.saveFrameToBuf()

		frame = cornerFrame

		nudgeMotor = None
		nudgeTime  = None
		if vc.lastFlowPnts is not None:
			pnts = vc.lastFlowPnts
			# Log.debug( 3*vc.height/4 )
			# Log.debug( pnt )
			
			if len(pnts) == 2 and abs(pnts[0][0][1] - pnts[1][0][1]) < 10:
				# condition where there are only 2 dots on the same horz
				# we don't wanna stop on the farthest tracked point
				pass
			elif pnts[0][0][1] > (3*vc.height/4)-25:
				Log.debug( "can't continue, gotta stop - corner" )
				return True
		for line in horz:
			if line[0] > vc.height-80 and line[1] == 255:
				Log.debug( "can't continue, gotta stop - line" )
				return True
		if intersect and vc.frameCount >= (lastNudge+10):
			if intersect > (vc.width/2 + 60):
				nudgeMotor = cl.M2
				nudgeTime  = 6
				circle( frame, (20, vc.height-20), 6, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 25):
				nudgeMotor = cl.M2
				nudgeTime  = 4
				circle( frame, (20, vc.height-20), 4, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 15):
				nudgeMotor = cl.M2
				nudgeTime  = 2
				circle( frame, (20, vc.height-20), 2, (0,0,255), 2 )
			elif intersect < (vc.width/2 - 60):
				nudgeMotor = cl.M1
				nudgeTime  = 6
				circle( frame, (20, vc.height-20), 6, (0,255,0), 2 )
			elif intersect < (vc.width/2 - 25):
				nudgeMotor = cl.M1
				nudgeTime  = 4
				circle( frame, (20, vc.height-20), 4, (0,255,0), 2 )
			elif intersect < (vc.width/2 - 15):
				nudgeMotor = cl.M1
				nudgeTime  = 2
				circle( frame, (20, vc.height-20), 2, (0,255,0), 2 )
		if nudgeMotor and nudgeTime:
			cl.flush()
			cl.nudge( nudgeMotor, nudgeTime )
			test = cl.readAndCheck()
			if not test:
				Log.warning( "nudge %s, %d not received D=" % (nudgeMotor, nudgeTime) )
			else:
				Log.info( "nudge %s, %d received!" % (nudgeMotor, nudgeTime) )
				lastNudge = vc.frameCount

def mainLoop():
	global nextTurn

	while True:
		Log.debug( "buffer loop" )
		while vc.frameBuf.size() < 5 and vc.lastFlowPnts is None and vc.captureFrame():
			lineFrame, intersect, horz = vc.findLines()
			cornerFrame = vc.trackCorners()
			vc.drawGrid( cornerFrame )
			vc.writeFrame( cornerFrame )
			if intersect:
				vc.saveFrameToBuf()

		# check allowed directions
		directions = vc.findTurns()
		Log.debug( directions )
		if len( directions ) == 0:
			Log.warning( "could not find directions, trying again.." )
			vc.reset()
			continue
		nextTurn = random.choice( directions )

		Log.debug( "sending start" )
		cl.flush()
		cl.start( 13 )
		test = cl.readAndCheck()
		if not test:
			Log.warning( "start not received D=" )
		else:
			Log.info( "start received!" )

		# go forward til we have to stop
		if not forwardMovement():
			# stop and reset
			Log.debug( "sending stop" )
			cl.flush()
			cl.stop()
			if not cl.readAndCheck():
				Log.warning( "stop not received D=" )
			else:
				Log.info( "stop received!" )
			delay( 100 )
			vc.reset()
			continue

		Log.debug( "sending stop" )
		cl.flush()
		cl.stop()
		if not cl.readAndCheck():
			Log.warning( "stop not received D=" )
		else:
			Log.info( "stop received!" )

		delay( 100 )

		# now we gotta turn
		if nextTurn == 'Left':
			Log.debug( "sending Left" )
			cl.flush()
			cl.turnLeft()
			delay( 4000 )
			if not cl.readAndCheck():
				Log.warning( "Left not received D=" )
			else:
				Log.info( "Left received!" )
		elif nextTurn == 'Right':
			Log.debug( "sending Right" )
			cl.flush()
			cl.turnRight()
			delay( 4000 )
			if not cl.readAndCheck():
				Log.warning( "Right not received D=" )
			else:
				Log.info( "Right received!" )
		elif nextTurn == 'Up':
			Log.debug( "sending Up" )
		elif nextTurn == 'Down':
			Log.debug( "sending Down" )
			cl.flush()
			cl.turnAround()
			delay( 4000 )
			if not cl.readAndCheck():
				Log.warning( "Turn around not received D=" )
			else:
				Log.info( "Turn around received!" )
		elif nextTurn == 'StopSign':
			Log.debug( "sending StopSign" )
			cl.flush()
			#cl.stop()
			if not cl.readAndCheck():
				Log.warning( "Stop sign not received D=" )
			else:
				Log.info( "Stop sign received!" )
		elif nextTurn == 'Destination':
			Log.debug( "sending Destination" )
			cl.flush()
			cl.stop()
			if not cl.readAndCheck():
				Log.warning( "Destination not received D=" )
			else:
				Log.info( "Destination received!" )

		# burn some frames
		Log.info( "burning frames.." )
		for i in range(10):
			vc.captureFrame()

		Log.info( "resetting video capture" )
		vc.reset()

if __name__ == '__main__':
	import sys, os
	from argparse import ArgumentParser
	from datetime import datetime
	global vc

	parser = ArgumentParser()
	parser.add_argument( "-v", "--verbose", help="log debug data", action="store_true" )
	parser.add_argument( "-c", "--console", help="log to console rather than a log file", action="store_true" )
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	args = parser.parse_args()

	st = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
	log_path = 'log/%s.log' % st
	
	kwargs = {}
	if args.verbose:
		kwargs['level'] = logging.DEBUG
	else:
		kwargs['level'] = logging.INFO
	if not args.console:
		kwargs['filename'] = log_path
	kwargs['format'] = '%(levelname)s %(module)s.%(funcName)s: %(message)s'
	kwargs['datefmt'] = '%H:%M:%S'
	
	logging.basicConfig( **kwargs )

	# log uncaught exceptions
	# thanks http://stackoverflow.com/a/8054179
	# def logException( type, value, tb ):
	# 	Log.exception( "Uncaught exception: {0}".format( str(value) ), exc_info=True )
	
	# sys.excepthook = logException
	vc = VideoCapture( outfile=args.outfile, fourcc=args.fourcc )
	cl.setup()

	# print "starting in 10 seconds..."
	# delay( 10000 )

	# spend some frames letting the camera warm up
	for i in range(10):
		vc.captureFrame()

	try:
		mainLoop()
	except KeyboardInterrupt:
		Log.info( "we're done here" )

	vc.cleanUp()
