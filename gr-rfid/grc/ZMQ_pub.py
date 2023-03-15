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
# socket.bind("tcp://127.0.0.2:%s" % port)
# Bind is for local endpoint, * or localhost. Not specific IP?
socket.bind("tcp://*:%s" % port)
# socket.bind("tcp://192.168.1.103:%s" % port)

while True:
	EPC = random.choice(['1', '0'])
	socket.send(bytes(EPC, 'utf-8'))
	print('Sent')
	time.sleep(0.3)
