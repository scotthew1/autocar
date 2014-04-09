#!/usr/bin/python

from bbio import *
from cv2 import circle
from videoLib import VideoCapture
import commandLib as cl
import logging

Log = logging.getLogger()

global vc
nextTurn = 'left'

def forwardMovement():
	lastNudge = 0
	intersect = None
	while vc.captureFrame():
		frame, intersect, horz = vc.findLines()
		nudgeMotor = None
		nudgeTime  = None
		mustStop = False
		for line in horz:
			if line[0] > vc.height-45 and line[1] == 255:
				Log.debug( "can't continue, gotta stop" )
				vc.drawGrid( frame )
				vc.writeFrame( frame )
				vc.saveFrameToBuf()
				return
		if intersect and vc.frameCount >= (lastNudge+15):
			if intersect > (vc.width/2 + 60):
				nudgeMotor = cl.M2
				nudgeTime  = 7
				circle( frame, (20, vc.height-20), 6, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 30):
				nudgeMotor = cl.M2
				nudgeTime  = 4
				circle( frame, (20, vc.height-20), 4, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 15):
				nudgeMotor = cl.M2
				nudgeTime  = 2
				circle( frame, (20, vc.height-20), 2, (0,0,255), 2 )
			elif intersect < (vc.width/2 - 60):
				nudgeMotor = cl.M1
				nudgeTime  = 7
				circle( frame, (20, vc.height-20), 6, (0,255,0), 2 )
			elif intersect < (vc.width/2 - 30):
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
		vc.drawGrid( frame )
		vc.writeFrame( frame )
		vc.saveFrameToBuf()

def mainLoop():
	global nextTurn

	try:
		while True:
			Log.debug( "buffer loop" )
			while vc.frameBuf.size() < 5 and vc.captureFrame():
				frame, intersect, horz = vc.findLines()
				vc.drawGrid( frame )
				vc.writeFrame( frame )
				if intersect:
					vc.saveFrameToBuf()

			Log.debug( "sending start" )
			cl.flush()
			cl.start( 13 )
			test = cl.readAndCheck()
			if not test:
				Log.warning( "start not received D=" )
			else:
				Log.info( "start received!" )

			# go forward til we have to stop
			forwardMovement()

			Log.debug( "sending stop" )
			cl.flush()
			cl.stop()
			if not cl.readAndCheck():
				Log.warning( "stop not received D=" )
 			else:
				Log.info( "stop received!" )

			# now we gotta turn
			if nextTurn == 'left':
				Log.debug( "sending left" )
				cl.flush()
				cl.turnLeft()
				if not cl.readAndCheck():
					Log.warning( "turn not received D=" )
 				else:
					Log.info( "turn received!" )

			# delay for turn and clear that buffer
			delay( 3000 )
			vc.frameBuf.clear()
	except KeyboardInterrupt:
		Log.info( "we're done here" )


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

	print "starting in 10 seconds..."
	delay( 10000 )

	mainLoop()
