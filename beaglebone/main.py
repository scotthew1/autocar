#!/usr/bin/python

from bbio import *
from cv2 import circle
from videoLib import VideoCapture
import commandLib as cl

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
			# print "horz:", line
			if line[0] > vc.height-45 and line[1] == 255:
				print "can't continue, gotta stop"
				vc.drawGrid( frame )
				vc.writeFrame( frame )
				vc.saveFrameToBuf()
				return
		if intersect and vc.frameCount >= (lastNudge+15):
			if intersect > (vc.width/2 + 60):
				print "BIGGER NUDGE M2!!"
				nudgeMotor = cl.M2
				nudgeTime  = 7
				circle( frame, (20, vc.height-20), 6, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 30):
				print "BIG NUDGE M2!!"
				nudgeMotor = cl.M2
				nudgeTime  = 4
				circle( frame, (20, vc.height-20), 4, (0,0,255), 2 )
			elif intersect > (vc.width/2 + 15):
				print "NUDGE M2!!"
				nudgeMotor = cl.M2
				nudgeTime  = 2
				circle( frame, (20, vc.height-20), 2, (0,0,255), 2 )
			elif intersect < (vc.width/2 - 60):
				print "BIGGER NUDGE M1!!"
				nudgeMotor = cl.M1
				nudgeTime  = 7
				circle( frame, (20, vc.height-20), 6, (0,255,0), 2 )
			elif intersect < (vc.width/2 - 30):
				print "BIG NUDGE M1!!"
				nudgeMotor = cl.M1
				nudgeTime  = 4
				circle( frame, (20, vc.height-20), 4, (0,255,0), 2 )
			elif intersect < (vc.width/2 - 15):
				print "NUDGE M1!!"
				nudgeMotor = cl.M1
				nudgeTime  = 2
				circle( frame, (20, vc.height-20), 2, (0,255,0), 2 )
		if nudgeMotor and nudgeTime:
			cl.flush()
			cl.nudge( nudgeMotor, nudgeTime )
			test = cl.readAndCheck()
			if not test:
				print "nudge not received D="
			else:
				print "nudge received!"
				lastNudge = vc.frameCount
		vc.drawGrid( frame )
		vc.writeFrame( frame )
		vc.saveFrameToBuf()

def mainLoop():
	global nextTurn

	try:
		while True:
			print "buffer loop"
			while vc.frameBuf.size() < 5 and vc.captureFrame():
				frame, intersect, horz = vc.findLines()
				vc.drawGrid( frame )
				vc.writeFrame( frame )
				if intersect:
					vc.saveFrameToBuf()

			print "sending start"
			cl.flush()
			cl.start( 13 )
			test = cl.readAndCheck()
			if not test:
				print "start not received D="
			else:
				print "start received!"

			# go forward til we have to stop
			forwardMovement()

			print "sending stop"
			cl.flush()
			cl.stop()
			if not cl.readAndCheck():
				print "stop not received D="
			else:
				print "stop received!"

			# now we gotta turn
			if nextTurn == 'left':
				print "sending left"
				cl.flush()
				cl.turnLeft()
				if not cl.readAndCheck():
					print "turn not received D="
				else:
					print "turn received!"

			# delay for turn and clear that buffer
			delay( 3000 )
			vc.frameBuf.clear()
	except KeyboardInterrupt:
		print "we're done here"


if __name__ == '__main__':
	from argparse import ArgumentParser
	global vc

	parser = ArgumentParser()
	parser.add_argument( "-o", "--outfile", help="output processed to a file" )
	parser.add_argument( "--fourcc", help="four character code to specify video output type", default="XVID" )
	args = parser.parse_args()

	vc = VideoCapture( outfile=args.outfile, fourcc=args.fourcc )
	cl.setup()

	delay( 10000 )

	mainLoop()
