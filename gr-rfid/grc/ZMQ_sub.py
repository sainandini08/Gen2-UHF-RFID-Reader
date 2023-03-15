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
	Present = socket.recv()
	print(Present)
	a = int.from_bytes(Present, "little")
	print(a)
