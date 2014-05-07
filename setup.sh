#!/bin/bash

# some setup stuff that should run each time
# needs sudo to run

# set properties for the webcam
v4l2-ctl -d /dev/video0 -c exposure_auto_priority=1
v4l2-ctl -d /dev/video0 -c exposure_auto=1
v4l2-ctl -d /dev/video0 -c exposure_absolute=100
v4l2-ctl -d /dev/video0 -c contrast=80
v4l2-ctl --list-ctrls

# get internet working
route add default gw 192.168.7.1