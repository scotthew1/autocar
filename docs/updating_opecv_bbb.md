getting opencv-2.4.8 on my bbb
==============================

* this was the error:
	``
	Traceback (most recent call last):
	  File “test.py", line 31, in <module>
	    surf = cv2.SURF(10000,1,1,0,0)
	AttributeError: 'module' object has no attribute ‘SURF’
	``

* tried [this][1] (opting for the more recent opencv-2.4.8), but compiling on the beaglebone was not possible because of memory constraints:

* went [here][2], to figure out how to cross compile for arm.

* I opted for the cross compiler that supported the Cortex-A8's hardware floating point operations:
	``sudo apt-get install gcc-arm-linux-gnueabihf``

* I ran into issues getting this this cross-compile to build the python library, so I had to copy the contents of `/usr/lib/python2.7/` to my vm as `/usr/lib/python2.7-arm/`

* I created my build folder within the opencv-2.4.8 source to take advantage of opencv's existing gnueabihf toolchain:
	``
	mkdir opencv-2.4.8/platforms/linux/buildhf/
	cd opencv-2.4.8/platforms/linux/buildhf/
	``

* The I ran cmake with these parameters:
	``
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D ENABLE_NEON=ON \
      -D WITH_XINE=ON \
      -D WITH_OPENGL=ON \
      -D WITH_TBB=ON \
      -D BUILD_EXAMPLES=ON \
      -D BUILD_NEW_PYTHON_SUPPORT=ON \
      -D WITH_V4L=ON \
      -D PYTHON_LIBRARY=/usr/lib/python2.7-arm/config-arm-linux-gnueabihf/libpython2.7.so \
      -D CMAKE_TOOLCHAIN_FILE=../arm-gnueabi.toolchain.cmake \
      -D CMAKE_INSTALL_PREFIX=~/opencv-2.4.8 \
      ../../..
	``

* And built the damn thing:
	``make && make install``

* This put a folder in my vm's home directory called opencv-2.4.8 which I copied to the beaglebone's home folder.

* On the beaglebone, I copied my carefully copied the new opencv library files to the beaglebone's /usr/lib:
	``
	cd ~
	sudo su
	cp opencv-2.4.8/lib/python2.7/dist-packages/* /usr/lib/python2.7/dist-packages/
	cp opencv-2.4.8/lib/pkgconfig/* /usr/lib/pkgconfig/
	cp opencv-2.4.8/lib/*.so.2.4.8 /usr/lib/
	``

* finally, I fixed the opencv library links to point to the new version wit this sweet one liner:
	``
	cd /usr/lib/ && sudo rm libopencv_*.so.2.4 && ls | grep 'libopencv_.*.so.2.4.8' | sed 's/\(.*\).8/ln -s \1.8 \1/' | sudo sh
	``

[1]:http://stackoverflow.com/a/18590112
[2]:http://docs.opencv.org/doc/tutorials/introduction/crosscompilation/arm_crosscompile_with_cmake.html