# commandLib.py is meant to prepare a string of bits that will
# be interpreted by the Arduino so that the robot can perform
# the commands sent by the BeagleBone.

from bbio import *  #for when the beaglebone is hooked up


def setup():
	"""
	Set up the UART communication to baud rate 9600
	"""
 	Serial1.begin(9600)

def stop():
	"""
	Stop the car
	"""
	command = 'a' + "000"
	Serial1.write(command)

def start( speed ): 
	"""
	Starts the car
	if speed is too high or negative, a ValueError exception is raised.
	"""
	if speed < 1 or speed > 99:
		raise ValueError
	if speed < 10:
		command = 'b' + '0' + str(speed) + '0'
	else:
		command = 'b' + str(speed) + '0'
	Serial1.write(command)

def leftTurn():
	"""
	Turn the car left 90 degrees
	"""
	command = 'c' + "000"
	Serial1.write(command)

def rightTurn():
	"""
	Turn the car right 90 degrees
	"""
	command = 'd' + "000"
	Serial1.write(command)

def turnAround():
	"""
	Turn the car around 180 degrees
	"""
	command = 'e' + "000"
	Serial1.write(command)

def increasePower( motor, speed ):   
	"""
	Increases power to a motor of choice
	if the motor input is malformed, a ValueError exception is raised.
	if the speed is too high or low, a ValueError exception is raised.
	"""
	if !isinstance(motor, basestring) or len(motor) != 2:
		raise ValueError
	if speed < 0 or speed > 9:
		raise ValueError
	command = 'f' + motor.decode("hex") + str(speed) + '0'
	Serial1.write(command)

def decreasePower( motor, speed ):  
	"""
	Decreases power to a motor of choice
	if the motor input is malformed, a ValueError exception is raised.
	if the speed is too high or low, a ValueError exception is raised.
	"""
	if !isinstance(motor, basestring) or len(motor) != 2:
		raise ValueError
	if speed < 0 or speed > 9:
		raise ValueError
	command = 'g' + motor.decode("hex") + str(speed) + '0'
	Serial1.write(command)

def reverse( speed ):  
	"""
	Reverses the car
	if speed is too high or negative, a ValueError exception is raised.
	"""
	if speed < 1 or speed > 99:
		raise ValueError
	if speed < 10:
		command = 'h' + '0' + str(speed) + '0'
	else:
		command = 'h' + str(speed) + '0'
	Serial1.write(command)
