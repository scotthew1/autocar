from bbio import *
import Adafruit_BBIO.GPIO as GPIO

def setup():
	GPIO.setup("P8_7", GPIO.OUT)	# RED
	GPIO.setup("P8_8", GPIO.OUT)	# GREEN
	GPIO.setup("P8_9", GPIO.OUT)	# BLUE

def LED():
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.LOW)
	print("CLEAR")
	delay(3000)
	GPIO.output("P8_7", GPIO.HIGH)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.LOW)
	print("RED")
	delay(3000)
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_9", GPIO.LOW)
	print("GREEN")
	delay(3000)
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.HIGH)
	print("BLUE")
	delay(3000)
	#GPIO.output("P8_5", GPIO.HIGH)
	#GPIO.output("P8_6", GPIO.HIGH)
	#GPIO.output("P8_8", GPIO.HIGH)
	#print("HIGH")
	#delay(3000)

run(setup,LED)
