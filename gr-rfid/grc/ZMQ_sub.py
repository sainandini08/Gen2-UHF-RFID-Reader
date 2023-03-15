import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)

print('Connecting to IP Address')
# Connect is for remote ip address of PUB server
socket.connect("tcp://127.0.0.1:5556")

# Subscribe to topic
socket.setsockopt(zmq.SUBSCRIBE, b'')  # subscribe to topic of all

running = True

while running:
	Tag = socket.recv()
	#print(Tag)
	if Tag and Tag == b'\x01':
		print("tag present")
	#Tag_int = int.from_bytes(Tag, "little")
	#print(Tag_int)
