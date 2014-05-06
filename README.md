Autocar - Self Driving Vehicle
==============================

![AutocarImg]

Autocar is a car-like robot built with the Matrix Robotics set that can navigate itself through a mock city grid using a USB webcam. See it in action [here][demo video].

Image Processing Quick Start
----------------------------

Even without the full robot setup, you can play with our image processing functions very simply. We tested this code on Ubuntu 13.04, but any system with Python2.7 and a webcam should theoretically work.

1. [Install OpenCV]. On Ubuntu this can be done simply as:
    ```
    sudo apt-get install python-opencv python-numpy
    ```
2. Clone this repo
    ```
    cd /install/path
    git clone https://github.com/scotthew1/autocar.git
    cd autocar/
    ```
3. Run an image processing function
    ```
    beaglebone/videoLib.py -s -f lines
    ```
    This will show a visualtion for findLines() which was used to keep Autocar
    in the lines on the road. There are other functions you can run. 
    `beaglebone/videoLib.py --help` will list available functions.

See [Hardware Setup] for more informaion on the hardware of Autocar.

See [Software Setup] for more information on running the code as a complete system.


List of Components
------------------

* [Matrix Robotics Base Set]
    * Matrix Controller
    * 2x Motors
    * [Rotacaster Wheel]
    * Battery pack
* [BeagleBone Black]
* [BeagleBone battery cape]
* [Arduino Uno]
* Arduino Matrix cape (custom made)
* [EOPD Sensor] (distance sensor, prototype version)
* [Logic Level Converter]
* RGB LED
* USB Webcam
    * Xbox Live camera (used during development)
    * Logitech C920 (used on demo day)

Special Thanks To...
--------------------
* Our awesome proffessors - Dr. Marcy, William Tetley, Michael Frasciello
* Our awesome TA - Matthew Scott
* [HiTechnic] for lending us the robotics set and access to prototype materials
* [Derek Molloy] for his excellent BeagleBone tutorials
* [Matthew Witherwax] for his posts on USB webcams with the BeagleBone and 
saving our asses in building OpenCV on the Beaglebone
* [PyBBIO]

[AutocarImg]:docs/img/autocar.jpg
[demo video]:http://youtu.be/uN0txue1ocM
[Hardware Setup]:docs/hardwareSetup.md
[Software Setup]:docs/softwareSetup.md
[Install OpenCV]:http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html
[Matrix Robotics Base Set]:http://matrixrobotics.com/products/
[Rotacaster Wheel]:http://www.hitechnic.com/cgi-bin/commerce.cgi?preadd=action&key=HRC2148
[BeagleBone Black]:http://beagleboard.org/Products/BeagleBone+Black
[BeagleBone battery cape]:http://elinux.org/CircuitCo:BeagleBone_Battery
[Arduino Uno]:http://arduino.cc/en/Main/arduinoBoardUno
[Logic Level Converter]:http://www.adafruit.com/products/757
[EOPD Sensor]:http://www.hitechnic.com/cgi-bin/commerce.cgi?preadd=action&key=NEO1048
[HiTechnic]:http://www.hitechnic.com/
[Derek Molloy]:http://derekmolloy.ie/
[Matthew Witherwax]:http://blog.lemoneerlabs.com/
[PyBBIO]:https://github.com/alexanderhiam/PyBBIO