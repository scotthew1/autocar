#!/usr/bin/python

from bbio import *
from videoLib import VideoCapture
import commandLib as cl

def mainLoop():
	vc = VideoCapture( outfile="../sample_video/camup3_movemnet.avi" )

	print "sending start"
	cl.start( 15 )
	test = cl.readAndCheck()
	print test
	if not test:
		print "start not received D="
	else:
		print "start received!"

	t0 = time.time()
	while vc.captureFrame() and vc.frameCount < 200:
		vc.writeFrame()

	t1 = time.time()
	tt = t1 - t0
	
	print "frames: %d" % vc.frameCount
	print "time: %f" % tt
	print "fps: %f" % (vc.frameCount/tt)

	# delay( 7000 )
	print "sending stop"
	cl.stop()
	if not cl.readAndCheck():
		print "stop not received D="
	else:
		print "stop received!"


if __name__ == '__main__':
	cl.setup()
	mainLoop()
