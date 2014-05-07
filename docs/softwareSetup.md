Software Setup
==============

Arduino
-------

**Prerequisites:**
* Arduino IDE
* MatrixController library folder

1. Before launching the Arduino IDE, move the MatrixController folder into the the Arduino folder on your computer. On my mac it's `~/Documents/Arduino/`

2. Launch the Arduino IDE and open `autocar/arduino/autocar_slave/autocar_slave.ino`

3. With the Arduino Uno connected to your computer via USB, press the `Upload` button in the Arduino IDE

4. If the upload was successful, you can disconnect the Arduino from your computer. **Note:** serial (UART) communication on the Arduino will not work while you have it connected via USB.

BeagleBone Black
----------------

**Prerequisites:**
* Ubuntu (or Ubuntu VM) on your computer to provide internet to the BeagleBone
* If you're not running Ubuntu on your computer, you might need to [install drivers]

1. For this project, we were running Ubuntu 13.04 on the BeagleBone installed on a 16GB micro SD. There is a chance this would work on the default Angstrom build, but all further steps will assume you have Ubuntu installed on your BeagleBone. To install Ubuntu on the BeagleBone, follow this [elinux tutorial] for Saucy 13.04.

2. Once you can ssh into the BeagleBone, you're going to want to provide internet access to the bone. If you're running Ubuntu on your host computer, you can run this to share internet to your bone:
    ```
    cd /path/to/autocar/
    sudo ./shareInternet.sh
    ```

    Then on the Beaglebone:
    ```
    route add default gw 192.168.7.1
    ```
    
    You should now have internet on the BeagleBone. Test by running:
    ```
    ping 8.8.8.8
    ```

3. As good practice, get any updates for Ubuntu
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```

4. In some of our testing, we noticed that Ubuntu on the BeagleBone was starting up a screen saver that was killing performance. Let's disable that before we forget. Open `/etc/xdg/lxsession/LXDE/autostart` with your editor of choice and delete the `xscreensaver` line.

5. Now we need to install OpenCV, It miiiiight be this easy:
    ```
    sudo apt-get install python-opencv python-numpy
    ```

    But we ran into some issues with the version of OpenCV that apt-get installed. If you run into any issues with OpenCV (performance wise or functions not working at all) then you're going to need to compile OpenCV from source. First remove the version of OpenCV that apt-get installed:
    ```
    apt-get --purge remove python-opencv
    ```
    
    Then follow this [awesome tutorial] for compiling OpenCV on the BeagleBone using distcc.
    
6. If you haven't already done so, clone this repo to your BeagleBone
    ```
    cd ~
    git clone https://github.com/scotthew1/autocar.git
    ```

7. Now you should be able to run some image processing functions on the BeagleBone!
    ```
    cd autocar/
    beaglebone/videoLib.py -f lines -o ~/test_video.avi -l 200
    ```
    
    Running the above function should output 200 frames of sample video to your home directory processed using the findLines() function.

**Caveates:**
* In order to power the webcam, the BeagleBone must be receiving 5V power. It will not receive 5V from your computer via USB. You must use a 5V AC power adapter or the BeagleBone battery cape (or provide 5V to the BeagleBone's 5V pin but be careful)
* When videoLib.py connects to the webcam, it initially spits out a bunch of errors. As long as it doesn't crash, it should run fine. Sometimes it does randomly crash, just try running it again and it should work.
* In order to use the `-s` flag with videoLib.py, you must have LXDE set up on your BeagleBone and you must shh into the bone with the `-X` option. However, running with the `-s` flag on the BeagleBone is extremely slow.

Communication
-------------

**Prerequisites:**
* The BeagleBone and the Arduino must be connected the the logic level converted according to the [Hardware Setup].
* The Arduino should be programmed and running as described above.
* You should be sharing internet to the BeagleBone as described above.

1. Follow the tutorial for [installing PyBBIO] on your BeagleBone.

2. Make sure the BeagleBone and arduino are communicating properly:
    ```
    cd ~/autocar
    beaglebone/simpleSerialTest.py
    ```

    You should see lines like `received: ackt`, if you do not, something is not working. Press `^C` to stop this program.
    
Running Autocar
---------------

Assuming you have followed all the previous steps including the Hardware Setup, it's time to try running Autocar!

1. shh into the BeagleBone, and run the setup script.
    ```
    cd ~/autocar
    sudo ./setup.sh
    ```

    This file sets up some default camera values. Depending on your lighting/enviromental conditions, you may need to modify these.
    
2. In order to run without a USB cable connected to the BeagleBone, start a screen session.
    ```
    screen -S autocar
    ```

3. Now run the main function
    ```
    sudo beaglebone/main.py 
    ```

    When you see the line `starting in 10 seconds...` detach from the screen session `^A d` and you're free to unplug the USB cable from the BeagleBone.
    
4. Autocar will now randomly drive around and stay within the lines of our [city grid]. If something goes wrong (Autocar gets hung up or tries to drive off the road) simply hold your hand over the camera and place Autocar at the center of an intersection. Once you remove your hand, Autocar should start running normally again.

5. When you're done running Autocar, hit the off switch (thus disabling the Arduino and Matrix Controller). Connect the BeagleBone nack to your computer via USB and ssh into the bone. Then reattach to the screen session
    ```
    screen -R autocar
    ```

    You can now press `^C` to stop main.py. A log file can be found in `autocar/logs/` that you can read through for debugging purposes.
    
Current Software Status
-----------------------

A general logic flow diagram of the main loop as it is currently implemented can be seen [here][logic flow].

In order to meet the deadline for our project, and to cope with some lighting issues that we experienced on demo day, some features have been removed from main.py. These features still exist in source code, but would need to be re-implemented in main.py. They include:
* Detecting arrows on the road and reading their direction. `findShapes()` in videoLib.py
* Making arrows so that they do not interfere with line detection. `maskcolors()` in videoLib.py
* Collision avoidance with the EOPD distance sensor. 
* Status indicators with the RGB LED. functions in ledLib.py

[install drivers]:http://beagleboard.org/Getting%20Started#step2
[elinux tutorial]:http://elinux.org/BeagleBoardUbuntu#Method_1:_Download_a_Complete_Pre-Configured_Image
[awesome tutorial]:http://blog.lemoneerlabs.com/3rdParty/Darling_BBB_30fps_DRAFT.html
[Hardware Setup]:hardwareSetup.md
[installing PyBBIO]:https://github.com/alexanderhiam/PyBBIO/wiki/Installing-PyBBIO
[city grid]:img/mongooseCity.png
[logic flow]:img/logicFlow.png
