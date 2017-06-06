# Copyright 2017 The Smith-Kettlewell Eye Research Institute
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Giovanni Fusco - giofusco@ski.org


"""
this file provides a simple example on how to use tne unified framework library to collect data from the accelerometer 
and the pupil labs eye tracker.
 Before running this, start the eye tracker server on the eye tracker machine
"""

import unified_framework as uf
import time

if __name__ == "__main__":

    # setting up filenames using current timestamp
    timestr = time.strftime("%Y%m%d-%H%M%S")
    trackerLogFile = 'eyeTracker_' + timestr + '.txt'
    IMULogFile = 'IMU_' + timestr + '.txt'

    eventsfilename = 'events_'+ timestr + '.txt'
    eventsLogfile = open(eventsfilename, 'w')

    imu_proc = uf.startIMUServer(IMULogFile, uf.IMU_TCP_PORT)

    # setting up communication channels
    print "[i] Opening Eye Tracker Socket..."
    eyeTrackerSocket = uf.setupSocket(uf.EYE_TRACKER_TCP_IP, uf.EYE_TRACKER_TCP_PORT)
    print "\t \t Socket opened."
    print "[i] Opening IMU Socket..."
    IMUSocket = uf.setupSocket(uf.IMU_TCP_IP, uf.IMU_TCP_PORT)
    print "\t \t Socket opened."

    print "[i] Setting Eye tracker log filename..."
    flag = uf.setLogFilename(eyeTrackerSocket, trackerLogFile)
    if flag == False:
        print "[e] !!! Filename not set !!!"
    else:
        print "\t \t Filename set."

    print "[i] Starting IMU logging..."
    flag = uf.startLogging(IMUSocket)
    if flag:
        print "\t \t IMU is logging."
        eventsLogfile.write('{:f} IMU START \n'.format(time.time()))
    else:
        print "[e] !!! IMU is NOT logging !!!"
        eventsLogfile.write('{:f} IMU START FAIL \n'.format(time.time()))


    print "[i] Starting Eye Tracker logging..."
    flag = uf.startLogging(eyeTrackerSocket)
    if flag:
        print "\t \t Eye Tracker is logging."
        eventsLogfile.write('{:f} EYETRACKER START \n'.format(time.time()))
    else:
        print "[e] !!! Eye Tracker is NOT logging !!!"
    eventsLogfile.write('{:f} EYETRACKER START FAIL \n'.format(time.time()))

    # collect data for 10 seconds
    t0 = time.time()
    eventsLogfile.write('{:f} START TRIAL \n'.format(time.time()))
    while time.time() - t0 < 10.: #
        # get eye tracker data
        gaze_position = uf.getEyeTrackerData(eyeTrackerSocket)


    print "[i] Stopping IMU logging..."
    uf.stopLogging(IMUSocket)
    print "\t \t IMU stopped."
    eventsLogfile.write('{:f} IMU STOPPED \n'.format(time.time()))

    print "[i] Stopping Eye Tracker logging..."
    uf.stopLogging(eyeTrackerSocket)
    print "\t \t Eye Tracker stopped."
    eventsLogfile.write('{:f} EYETRACKER STOPPED \n'.format(time.time()))

    # terminate communication and services
    uf.terminateLogging(eyeTrackerSocket)
    uf.terminateLogging(IMUSocket)

    # terminate and wait for the imu_server process to finish
    uf.terminateIMUServer(imu_proc)


