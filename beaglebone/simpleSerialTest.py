from bbio import *

def setup():
	"""
	Set up the UART communication to baud rate 9600
	"""
	Serial2.begin(9600)
	print "setup"

def loop():
	data1 = "tbcd"
	print "sending: %s" % data1
	Serial2.flush()
	num = Serial2.write(data1)
	print "bytes written: %s" % num
	delay(100)

	while Serial2.available():	
		# There's incoming data
		data = ''
		while( Serial2.available() ):
			data += Serial2.read()
		print "received: %s" % data

run( setup, loop )