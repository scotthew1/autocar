# commandLib.py is meant to prepare a string of bits that will
# be interpreted by the Arduino so that the robot can perform
# the commands sent by the BeagleBone.

from bbio import *  #for when the beaglebone is hooked up

#Set Serial1 to a 9600 baud rate
def setup():

 	Serial1.begin(9600)

def Stop ():

	command = 'a' + "000"
	Serial1.write(command)

def Start (speed): # Starts the car, if speed is too high or negative exception is raised.

	if speed < 0 or speed > 100:
	raise ValueError
	command = 'b' + str(speed)
	Serial1.write(command)

def leftTurn ():

	command = 'c' + "000"
	Serial1.write(command)

def rightTurn ():

	command = 'd' + "000"
	Serial1.write(command)

def turnAround ():

	command = 'e' + "000"
	Serial1.write(command)

def increasePower (motor, speed):   # Increases power to a motor of choice, if the speed is too high or low
									# an exception is raised.
	if speed < 0 or speed > 9:
	raise ValueError
	command = 'f' + "01".decode("hex") + str(speed)
	Serial1.write(command)

def decreasePower (motor, speed):  # Decreases power to a motor of choice, if the speed is too high or low
								   # an exception is raised.
	if speed < 0 or speed > 9:
	raise ValueError
	command = 'g' + "01".decode("hex") + str(speed)
	Serial1.write(command)

def Reverse (speed):  # Reverses the car, if the speed is too high or negative, an exception is raised.

	if speed < 0 or speed > 100:
	raise ValueError
	command = 'h' + str(speed)
	Serial1.write(command)
