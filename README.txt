 			=== Short practical guide to the UNIFIED FRAMEWORK ===
				Giovanni Fusco, giofusco@ski.org

The UNIFIED FRAMEWORK library handles socket connections between the Pupil Labs eye tracker and the LPMS-CURS2 v1.0 IMU.
Tested on Linux Ubuntu/Debian 64 bit.

The library has been tested with the current layout. The eye tracker is running on a Linux machine connected to a central computer through ethernet cable. The connection between the two computers has to be set so that both IP addresses of the machines are in the same subnet (e.g. 10.0.0.1 and 10.0.0.2, where 10.0.0.X defines the subnet).

The IMU is connected to the central computer via USB cable. Serial connections over USB appear under the /dev/ttyUSB* name in Linux Ubuntu. Make sure to take note of the correct name of the ttyUSB device every time you plug the IMU. If the IMU has been the last USB device you connected to the computer, you can find out which is the name by running ls -al /dev/ttyUSB* from a terminal and pick the one with the most recent time.


The UNIFIED FRAMEWORK is not guaranteed to work with different hardware versions or different OSs.
The eye tracker communication has been tested with the version of the Pupil Capture software available at the time 0.9.6.
The library is not guaranteed to work on a different version of the capture software.

** Future compatibility is not supported by the author.

The UNIFIED FRAMEWORK and all its components are released under the Apache License v2.0. 
The Apache License allows anyone to freely use, modify, and distribute any Apache licensed product.
For more info https://www.apache.org/licenses/


==================  HOW TO RUN THE EXAMPLE.py ===========================================

Example.py shows how to set up the connections with the IMU and the eye Tracker, log the data and how to grab the 3d gaze positions at runtime.

1) On the eye tracker laptop: start the eye pupil capture software, then launch eyeTracker_server.py
2) On the IMU/Stimuli computer: launch example.py to test that the connections are working.

Step 1 is always required, even when writing your own code.
Make sure the IMU port is corrected set up in the unified framework header section (line 26 of unified_framework.py)
the current value is set to IMU_TTY = '/dev/ttyUSB0'


======================

WARNING:
For security reasons, if your code crashes sockets may refuse to reconnect again right away. It usually takes less than a minute of cool off period for the socket to be accepting connections again. 
Keep this in mind when testing your code, refused connections after a crash or in general improper socket closing are normal. 
