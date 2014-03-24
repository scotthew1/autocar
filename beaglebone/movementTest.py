#!/usr/bin/python

from bbio import *
import commandLib as cl

def mainLoop():
	cl.start( 50 )
	delay( 100 )
	msg = cl.read()
	if msg != "ackb":
		print "start not received D="
	else:
		print "start received!"
	delay( 5000 )
	cl.stop()
	delay( 100 )
	msg = cl.read()
	if msg != "acka":
		print "stop not received D="
	else:
		print "stop received!"


if __name__ == '__main__':
	cl.setup()
	mainLoop()
