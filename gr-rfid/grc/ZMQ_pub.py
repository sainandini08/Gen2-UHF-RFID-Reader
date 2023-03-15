from __future__ import unicode_literals
import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
	port = sys.argv[1]
	int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
	TAG_PRESENT = random.choice([1, 0])
	socket.send(bytes([TAG_PRESENT]))
	print('Sent')
	time.sleep(0.1)
