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

import time
from time import sleep
import socket
import subprocess
import json
# default servers parameters
EYE_TRACKER_TCP_IP = '10.0.0.1'
EYE_TRACKER_TCP_PORT = 11000
IMU_TCP_IP = '127.0.0.1'
IMU_TCP_PORT = 10000
IMU_TTY = '/dev/ttyUSB0'

BUFFER_SIZE = 1024


# starts the UMI logging service and return the handle of the process.
def startIMUServer(IMULogFile, tcp_port = IMU_TCP_PORT):
    # starting IMU server
    print "[i] Starting IMU Server..."
    imu_server_args = ['./IMU_Server', str(tcp_port), IMU_TTY, IMULogFile]
    imu_proc = subprocess.Popen(imu_server_args)
    sleep(0.5)
    print "\t \t Server started."
    return imu_proc

def setLogFilename(socket, filename):
    # setup log files
    socket.send('SETFILE')
    # wait for server acknowledgment
    data = socket.recv(BUFFER_SIZE)
    if data == 'ACK_SETFILE':
        socket.send(filename)
        data = socket.recv(BUFFER_SIZE)
        if data == 'ACK_SETFILE_DONE':
            return True
        else:
            return False

def setupSocket(tcp_ip, tcp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcp_ip, tcp_port))
    return s

def startLogging(socket):
    socket.send('START')
    data = socket.recv(BUFFER_SIZE)
    if data == 'ACK_START':
        return True
    else:
        return False

def getEyeTrackerData(socket):
    data_buff = socket.recv(BUFFER_SIZE)
    words = []
    if len(data_buff) > 0:
        data = data_buff.split()
        return data
        # print '@{:f}'.format(time.time()) + ' - ' + data

def stopLogging(socket):
    socket.send('STOP')
    data = socket.recv(BUFFER_SIZE)
    if data == 'ACK_STOP':
        return True
    else:
        return False

def terminateLogging(socket):
    socket.send('QUIT')
    data = socket.recv(BUFFER_SIZE)
    socket.close()
    if data == 'ACK_QUIT':
        return True
    else:
        return False

def terminateIMUServer(imu_proc_handle):
    imu_proc_handle.terminate()
    imu_proc_handle.wait()
