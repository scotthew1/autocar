#!/bin/bash

# some setup stuff that should run each time
# needs sudo to run

<<<<<<< HEAD
# detect the webcam
# modprobe uvcvideo

=======
>>>>>>> c7c067c09692bfcce408cae6fca523150f9ebc06
# set properties for the webcam
v4l2-ctl -d /dev/video0 -c exposure_auto_priority=1
v4l2-ctl -d /dev/video0 -c exposure_auto=1
v4l2-ctl -d /dev/video0 -c exposure_absolute=100
v4l2-ctl -d /dev/video0 -c contrast=80
v4l2-ctl --list-ctrls

# get internet working
<<<<<<< HEAD
route add default gw 192.168.7.1

# i was annoyed with the time not being current, and couldnt get ntp working
# this is hacky and gets the time through ssh from my personal server
# without the proper config files, this won't work on a clean install
date --set="`ssh bender -o ConnectTimeout=3 -F /home/ubuntu/.ssh/config -i /home/ubuntu/.ssh/id_rsa date`"
=======
route add default gw 192.168.7.1
>>>>>>> c7c067c09692bfcce408cae6fca523150f9ebc06
