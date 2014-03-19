#!/usr/bin/python

# serial_echo.py - Alexander Hiam - 4/15/12
# 
# Prints all incoming data on Serial2 and echos it back.
# 
# Serial2 TX = pin 21 on P9 header
# Serial2 RX = pin 22 on P9 header
# 
# This example is in the public domain

from bbio import *
#from bitstring import *
temp = 0;

def setup():
  # Start Serial2 at 9600 baud:
  Serial1.begin(9600)


def loop():
  #a = BitArray('0xaa')
  #Serial2.write(a.hex)
  global temp
  data1 = "01".decode("hex")
  print data1
  delay(200)
  if (temp == 0):
    Serial1.write(data1)
    #temp = 1
    delay(5000)
    print "Data Sent:\n '%s'" % data1.decode("ascii")

  if (Serial1.available()):
    # There's incoming data
    data = ''
    while(Serial1.available()):
      # If multiple characters are being sent we want to catch
      # them all, so add received byte to our data string and 
      # delay a little to give the next byte time to arrive:
      data += Serial1.read()
      delay(200)
      temp = 0;

    # Print what was sent:
    print "Data received:\n  '%s'" % data
    # And write it back to the serial port
    #a = BitArray('0xaa')
    #Serial2.write(a.hex)
  # And a little delay to keep the Beaglebone happy:

  delay(200)

run(setup, loop)
