#!/bin/bash

# some setup stuff that should run each time
# needs sudo to run

# detect the webcam
modprobe uvcvideo

# get internet working
route add default gw 192.168.7.1

# i was annoyed with the time not being current, and couldnt get ntp working
# this is hacky and gets the time through ssh from my personal server
# without the proper config files, this won't work on a clean install
date --set="`ssh bender -F /home/ubuntu/.ssh/config -i /home/ubuntu/.ssh/id_rsa date`"
