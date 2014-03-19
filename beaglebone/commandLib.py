#!/usr/bin/python
import sys
import time 

def Stop ():

	choice = "0000"
	return choice

def Start (speed):

	choice = "0001"
	choice = choice + speed
	return choice

def leftTurn ():

	choice = "0010"
	return choice

def rightTurn ():

	choice = "0011"
	return choice

def turnAround ():

	choice = "0100"
	return choice

def increasePower (speed):

	choice = "0101"
	return choice

def decreasePower (speed):

	choice = "0110"
	return choice