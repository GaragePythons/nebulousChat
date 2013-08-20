from enum import enum
from serializing import serialize
import networking
import time

HOST, PORT = "localhost", 9999

keywords = [("nick")]

def timestamp():
    return time.time()

def dummyInputField(rawInput, socket):
    serializedStuff = serialize((rawInput, timestamp()))
    print type(serializedStuff)
    networking.send(serializedStuff, socket)

if __name__ == "__main__":
    # Connect to server.
    socket = networking.connect((HOST, PORT))

    # Wait for user to type messages until user presses Ctrl-C, then quit.
    try:
        while True:
            dummyInputField(raw_input(), socket)
    except KeyboardInterrupt:
        socket.close()
        print "\n[Closing socket and quitting.]"
