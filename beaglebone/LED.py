from bbio import *
import Adafruit_BBIO.GPIO as GPIO

def setup():
	GPIO.setup("P8_7", GPIO.OUT)	# RED
	GPIO.setup("P8_8", GPIO.OUT)	# GREEN
	GPIO.setup("P8_9", GPIO.OUT)	# BLUE

def LED():
	print("CLEAR")
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.LOW)
	delay(3000)
	print("RED")
	GPIO.output("P8_7", GPIO.HIGH)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.LOW)
	delay(3000)
	print("GREEN")
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_9", GPIO.LOW)
	delay(3000)
	print("BLUE")
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.HIGH)
	delay(3000)
	print("GREEN + RED")
	GPIO.output("P8_7", GPIO.HIGH)
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_9", GPIO.LOW)
	delay(3000)
	print("GREEN + BLUE")
	GPIO.output("P8_7", GPIO.HIGH)
	GPIO.output("P8_8", GPIO.LOW)
	GPIO.output("P8_9", GPIO.HIGH)
	delay(3000)
	print("RED + BLUE")
	GPIO.output("P8_7", GPIO.LOW)
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_9", GPIO.HIGH)
	delay(3000)
	print("GREEN + RED + BLUE")
	GPIO.output("P8_7", GPIO.HIGH)
	GPIO.output("P8_8", GPIO.HIGH)
	GPIO.output("P8_9", GPIO.HIGH)
	delay(3000)

run(setup,LED)
