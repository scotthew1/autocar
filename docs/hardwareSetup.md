Hardware Setup
==============

Vehicle Construction
--------------------

Autocar was build using the Matrix Robotics base kit. The two main wheels were located at the front of the car, and a single rotacaster wheel supported the back. This allowed for easy turning. Autocar was designed such that all of our components fit neatly on the car: Matrix controller on the bottom, Arduino and BeagleBone on the mid section, and the battery pack on top. The camera was mounted above the battery pack near the center of the Autocar, which gave the best field of view.

Component Diagram
-----------------

![component diagram]

**Notes:**
* The Matrix Robotics kit designed to be used with a Lego NXT 'brain'. We did not want to be limited to this kind of controller. The fine folks at HiTechnic have been devoloping means to use an Arduino in place of the NXT 'brain'. The Arduino Shield in this diagram is a prototype that allows the Arduino to act in place of the 'brain'.
* The Arduino communicates to the Matrix controller usng I2C.
* The BeagleBone communicates to the Arduino via the logic level converter using UART

Logic Level Converter
---------------------

The BeagleBone and the Arduino run at different voltages (3.3V and 5V respectively). As a result, we needed a logic level converter to make sure each controller recieved a signal in the voltage it expected. The converter was wired according to the following diagram:

![logic converter diagram]

Power
-----

The BeagleBone Black was powered using a BeagleBone battery cape. With 4 batteries inserted, this provided power to the 5V pin of the BeagleBone. Although the BeagleBone itself runs at 3.3V, 5V was needed to provide power to the webcam via the USB port.

The Arduino and the Matrix controller were powered by the 10.2V battery pack included with the Matrix Robotics set. In order to power both controllers (and to provide a simple on/off switch) we wired the batter as such:

![power diagram]

LED
---

An RGB LED was connected to the BeagleBone to provide status indicators when Autocar was running autonomously. The LED was connected with pull-up resistors to the beaglebone as follows (numbers indicate pins on the BeagleBone):

![LED diagram]

[component diagram]:img/components.png
[logic converter diagram]:img/levelConverter.png
[power diagram]:img/power.png
[LED diagram]:img/rgbLed.png