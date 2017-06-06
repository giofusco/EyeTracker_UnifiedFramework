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

import socket
import sys
import time
from time import sleep
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:

    # Send data
    message = 'START'
    print >> sys.stderr, 'sending "%s"' % message
    t0 = time.time()
    sock.sendall(message)
    t1 = time.time()

    print "Dt = ",t1-t0

    # Look for the response
    amount_received = 0
    amount_expected = len('ACK')

    t0 = time.time()
    while amount_received < amount_expected:
        data = sock.recv(3)
        amount_received += len(data)
    t1 = time.time()
    print "Dt = ", t1 - t0
    print >> sys.stderr, 'received "%s"' % data

    sleep(3)

    message = 'STOP'
    print >> sys.stderr, 'sending "%s"' % message
    t0 = time.time()
    sock.sendall(message)
    t1 = time.time()

    # Look for the response
    amount_received = 0
    amount_expected = len('ACK')
    t0 = time.time()
    while amount_received < amount_expected:
        data = sock.recv(3)
        amount_received += len(data)
    t1 = time.time()
    print "Dt = ", t1 - t0
    print >> sys.stderr, 'received "%s"' % data

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()
