# commandLib.py is meant to prepare a string of bits that will
# be interpreted by the Arduino so that the robot can perform
# the commands sent by the BeagleBone.

from bbio import *  #for when the beaglebone is hooked up

# comment this out when not demoing
DEMO = False

M1 = "01" # right
M2 = "02" # left
lastCall = None
delayAfterWrite = 50

def setup():
	"""
	Set up the UART communication to baud rate 9600
	"""
	Serial2.begin(9600)
	print "setup"

def flush():
	"""
	Clears out any existing messages
	"""
	Serial2.flush()

def read():
	"""
	Read data from the arduino
	"""
	data = None
	if Serial2.available():
		data = ''
		while( Serial2.available() ):
			data += Serial2.read()
			delay(5)
	return data

def getLastAck():
	"""
	Returns the acknowledgment expected from the last command sent
	"""
	if lastCall:
		return "ack" + lastCall
	else:
		return None

def readAndCheck():
	"""
	Reads data from the arduino and checks that it matches the 
	expected acknowledgment
	"""
	msg = read()
	ack = getLastAck()
	if not msg or not ack:
		return None
	elif msg == ack:
		if DEMO: print "message received! " + msg
		return True
	else:
		print "unexpected acknowledgment: " + msg
		return False

def test():
	"""
	Test the connection to the arduino
	"""
	global lastCall
	command = 't' + '000'
	print 'send command: %s' % command
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 't'
	if DEMO: readAndCheck()


def stop():
	"""
	Stop the car
	"""
	global lastCall
	command = 'a' + "000"
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'a'
	if DEMO: readAndCheck()

def start( speed ): 
	"""
	Starts the car
	if speed is too high or negative, a ValueError exception is raised.
	"""
	global lastCall
	if speed < 1 or speed > 99:
		raise ValueError
	if speed < 10:
		command = 'b' + '0' + str(speed) + '0'
	else:
		command = 'b' + str(speed) + '0'
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'b'
	if DEMO: readAndCheck()

def leftTurn():
	"""
	Turn the car left 90 degrees
	"""
	global lastCall
	command = 'c' + "000"
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'c'
	if DEMO: readAndCheck()

def rightTurn():
	"""
	Turn the car right 90 degrees
	"""
	global lastCall
	command = 'd' + "000"
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'd'
	if DEMO: readAndCheck()

def turnAround():
	"""
	Turn the car around 180 degrees
	"""
	global lastCall
	command = 'e' + "000"
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'e'
	if DEMO: readAndCheck()

def increasePower( motor, speed ):   
	"""
	Increases power to a motor of choice
	if the motor input is malformed, a ValueError exception is raised.
	if the speed is too high or low, a ValueError exception is raised.
	"""
	global lastCall
	if not isinstance(motor, basestring) or len(motor) != 2:
		raise ValueError
	if speed < 0 or speed > 9:
		raise ValueError
	command = 'f' + motor.decode("hex") + str(speed) + '0'
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'f'
	if DEMO: readAndCheck()

def decreasePower( motor, speed ):  
	"""
	Decreases power to a motor of choice
	if the motor input is malformed, a ValueError exception is raised.
	if the speed is too high or low, a ValueError exception is raised.
	"""
	global lastCall
	if not isinstance(motor, basestring) or len(motor) != 2:
		raise ValueError
	if speed < 0 or speed > 9:
		raise ValueError
	command = 'g' + motor.decode("hex") + str(speed) + '0'
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'g'
	if DEMO: readAndCheck()

def reverse( speed ):  
	"""
	Reverses the car
	if speed is too high or negative, a ValueError exception is raised.
	"""
	global lastCall
	if speed < 1 or speed > 99:
		raise ValueError
	if speed < 10:
		command = 'h' + '0' + str(speed) + '0'
	else:
		command = 'h' + str(speed) + '0'
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'h'
	if DEMO: readAndCheck()

def nudge( motor, nudgeTime=5 ):
	"""
	Nudges the car slight left or right depending on the motor selected.
	"""
	global lastCall
	if nudgeTime < 1 or nudgeTime >9
		raise ValueError
	if not isinstance(motor, basestring) or len(motor) != 2:
		raise ValueError
	command = 'n' + motor.decode("hex") + str(nudgeTime) + '0'
	Serial2.write( command )
	delay( delayAfterWrite )
	lastCall = 'n'
	if DEMO: readAndCheck()

def obj_det( speed ):
	"""
	If the arduino detects an object: reverse; stop; 180-turn; forward;
	"""
	global lastCall

	reverse(speed)
	delay(1000)
	turnAround()
	delay(1000)
	start(speed)
