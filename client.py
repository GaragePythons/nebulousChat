import socket
import sys

HOST, PORT = "localhost", 9999

def send(data):
    try:
        # Connect to server and send data
        sock = socket.create_connection((HOST, PORT))
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()
        print "[Closed socket]"

# Wait for messages until user presses Ctrl-C, then quit.
try:
    while(True):
        send(raw_input())
finally:
    print "\nQuitting."

print "Sent:     {}".format(data)
print "Received: {}".format(received)