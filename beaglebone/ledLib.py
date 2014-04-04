from bbio import *
import Adafruit_BBIO.GPIO as GPIO

OFF = (0,0,0)
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)
YELLOW = (1,1,0)
PURPLE = (1,0,1)

def setup():
	GPIO.setup("P8_7", GPIO.OUT)	# RED
	GPIO.setup("P8_8", GPIO.OUT)	# GREEN
	GPIO.setup("P8_9", GPIO.OUT)	# BLUE

def LED(color = OFF):
	GPIO.output("P8_7", color[0])
	GPIO.output("P8_8", color[1])
	GPIO.output("P8_9", color[2])