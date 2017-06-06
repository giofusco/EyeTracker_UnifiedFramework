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

import json
import socket
import sys
import threading
import zmq
from msgpack import loads
import time
import os
TCP_IP = '10.0.0.1'
TCP_PORT = 11000
BUFFER_SIZE = 1024

def print_title():
    os.system('clear')
    print " \t\t\t\t **** SKERI Pupil labs Eye Tracker Server **** \n \t\t\t\t       Giovanni Fusco - giofusco@ski.org "
    print "\n \t\t Current Server configuration"
    print "\t\t [IP address] ", TCP_IP
    print "\t\t [TCP port] ", TCP_PORT
    print "\t\t [Buffer Size] ", BUFFER_SIZE
    print "\n \t \t \t [Note] Did you start Pupil Capture?"

#eye tracker communication thread
class FuncThread(threading.Thread):
    def __init__(self, clientConnection, trackerTopic, logfilename):
        threading.Thread.__init__(self)
        self.connection = clientConnection
        self.trackerTopic = trackerTopic
        # change this if eyetracker is on a different machine
        self.trackerIP = '127.0.0.1'
        self.logfilename = logfilename
        self.logfile = open(self.logfilename, 'w')

        self.context = zmq.Context()
        self.log = True
        # open a req port to talk to pupil
        req_port = "50020"  # same as in the pupil remote gui
        self.req = self.context.socket(zmq.REQ)
        self.req.connect("tcp://{}:{}".format(self.trackerIP, req_port))
        # ask for the sub port
        self.req.send_string('SUB_PORT')
        self.sub_port = self.req.recv_string()
        # open a sub port to listen to pupil
        self.sub = self.context.socket(zmq.SUB)
        self.sub.connect("tcp://{}:{}".format(self.trackerIP, self.sub_port))
        self.sub.setsockopt_string(zmq.SUBSCRIBE, unicode(trackerTopic))
        # sub.setsockopt_string(zmq.SUBSCRIBE, 'notify.')
        # sub.setsockopt_string(zmq.SUBSCRIBE, 'logging.')
        # sub.setsockopt_string(zmq.SUBSCRIBE, 'surface')
        # packID = np.array([1])
        # or everything:
        # sub.setsockopt_string(zmq.SUBSCRIBE, '')
        self.req.send_string('T {:f}'.format(time.time()))
        # print
        print(self.req.recv_string())

    def run(self):
        while self.log:
            # Receive ZMQ message
            t0 = time.time()
            topic = self.sub.recv_string()
            msg = self.sub.recv()
            msg = loads(msg, encoding='utf-8')
            t1 = time.time()
            # print "DeltaT = ", t1 - t0
            # print("\n{:f}: {}".format(msg['timestamp'], msg['eye_centers_3d']))
            # dataLocal = "\n{:f}: {}".format(msg['timestamp'], msg['eye_centers_3d'])
            dataSend = '{:f} '.format(msg['timestamp'])
            if msg['gaze_normals_3d'].has_key(0):
                dataSend += '0 ' + str(msg['gaze_normals_3d'][0][0]) + ' ' + str(msg['gaze_normals_3d'][0][1]) + ' ' + \
                           str(msg['eye_centers_3d'][0][2])
            if msg['eye_centers_3d'].has_key(1):
                dataSend += ' 1 ' + str(msg['gaze_normals_3d'][1][0]) + ' ' + str(msg['gaze_normals_3d'][1][1]) + ' ' + \
                           str(msg['gaze_normals_3d'][1][2])
            self.logfile.write(dataSend+'\n')

            # dataSend = "\n{}".format(msg['eye_centers_3d'])
            # print len(data)
            self.connection.sendall(dataSend) #send it to the client


print_title()

#setup socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
threads = list()
logfilename = 'log.txt'
print "\n [i] Server Ready."
print "\t >> Waiting for client to connect..."
conn, addr = s.accept()

print '[i] Client Connected from IP:', addr

while 1:
    data = conn.recv(BUFFER_SIZE)
    t = time.time()

    # set log file name
    if data == "SETFILE":
        # send ack, wait for filename
        conn.send("ACK_SETFILE")
        data = conn.recv(BUFFER_SIZE)
        logfilename = data
        t = time.time()
        print >> sys.stderr, '[@{:f}][i] Log filename set to '.format(t)
        print >> sys.stderr, '\t\t', logfilename
        conn.send("ACK_SETFILE_DONE")

    if data == "START":
        print >> sys.stderr, '[{:f}][i] Starting Tracker Thread... '.format(t)
        thread1 = FuncThread(conn, "gaze", logfilename)
        threads.append(thread1)
        t = time.time()
        thread1.start()
        print >> sys.stderr, '[@{:f}][i] Thread Launched. Send STOP to stop.'.format(t)
        conn.send("ACK_START")
    elif data == "STOP":
        print >> sys.stderr, '[@{:f}][i] Stopping tracker thread...'.format(t)
        for thread in threads:
            thread.log = False
            thread.join()
            t = time.time()
        print >> sys.stderr, '[@{:f}][i] Thread Stopped.'.format(t)
        conn.send("ACK_STOP")
    elif data == "QUIT":
        print >> sys.stderr, '[i] Quitting. \n Ciao!'
        conn.send("ACK_QUIT")
        conn.close()
        break

conn.close()


