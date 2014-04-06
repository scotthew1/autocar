#!/usr/bin/python

from bbio import *
from cv2 import circle
from videoLib import VideoCapture
import commandLib as cl


nudgeHold = 10

def mainLoop():
	vc = VideoCapture( outfile="sample_video/nudge_movement_imp.avi" )
	lastNudge = 0

	intersect = None
	print "startup loop"
	while vc.frameBuf.size() < 5 and vc.captureFrame():
		frame, intersect = vc.findLines()
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

	# t0 = time.time()
	while vc.captureFrame() and vc.frameCount < 100:
		frame, intersect = vc.findLines()
		nudgeMotor = None
		nudgeTime  = None
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


	# t1 = time.time()
	# tt = t1 - t0
	
	# print "frames: %d" % vc.frameCount
	# print "time: %f" % tt
	# print "fps: %f" % (vc.frameCount/tt)

	# delay( 7000 )
	print "sending stop"
	cl.flush()
	cl.stop()
	if not cl.readAndCheck():
		print "stop not received D="
	else:
		print "stop received!"

def simpleNudgeTest():
	print "sending start"
	cl.flush()
	cl.start( 13 )
	test = cl.readAndCheck()
	if not test:
		print "start not received D="
	else:
		print "start received!"

	delay( 9000 )
	print "nudging"
	cl.flush()
	cl.nudge( cl.M1 )
	test = cl.readAndCheck()
	if not test:
		print "nudge not received D="
	else:
		print "nudge received!"

	delay( 3000 )
	print "sending stop"
	cl.flush()
	cl.stop()
	if not cl.readAndCheck():
		print "stop not received D="
	else:
		print "stop received!"

def testCapture():
	vc = VideoCapture( outfile="sample_video/other_side_test3.avi" )

	while vc.captureFrame():
		vc.writeFrame()
		vc.saveFrameToBuf()
		if vc.frameCount > 50:
			break

	print "sending start"
	cl.flush()
	cl.start( 13 )
	test = cl.readAndCheck()
	if not test:
		print "start not received D="
	else:
		print "start received!"

	while vc.captureFrame():
		vc.writeFrame()
		vc.saveFrameToBuf()
		if vc.frameCount > 250:
			break

	delay( 3000 )
	print "sending stop"
	cl.flush()
	cl.stop()
	if not cl.readAndCheck():
		print "stop not received D="
	else:
		print "stop received!"


if __name__ == '__main__':
	cl.setup()
	# testCapture()
	# simpleNudgeTest()
	mainLoop()
