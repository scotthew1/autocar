#!/usr/bin/python

from bbio import *
from videoLib import VideoCapture
import commandLib as cl

def mainLoop():
	vc = VideoCapture( outfile="sample_video/nudge_movement0.avi" )
	lastNudge = 0

	intersect = None
	print "startup loop"
	while intersect is None and vc.captureFrame():
		frame, intersect = vc.findLines()

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
		if intersect and intersect > (vc.width/2 + 20) and vc.frameCount >= (lastNudge+10):
			print "NUDGE M2!!"
			cl.flush()
			cl.nudge( cl.M2 )
			test = cl.readAndCheck()
			if not test:
				print "nudge not received D="
			else:
				print "nudge received!"
				lastNudge = vc.frameCount
		elif intersect and intersect < (vc.width/2 - 20) and (vc.frameCount >= lastNudge+10):
			print "NUDGE M1!!"
			cl.nudge( cl.M1 )
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
	testCapture()
	# simpleNudgeTest()
	# mainLoop()
