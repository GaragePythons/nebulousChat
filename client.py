from enum import enum
from serializing import serialize
import queries as q
import networking as n
import time

HOST, PORT = "localhost", 9999

keywords = [("nick")]

def timestamp():
    return time.time()

def dummyInputField(socket):
    while True:
        newMessage = q.Message()
        newMessage.messageString = raw_input()
        newMessage.timestamp = timestamp()
        n.sendFromClient(serialize(newMessage), socket)
        n.pullMessageList()

if __name__ == "__main__":
    # Connect to server.
    socket = n.connect((HOST, PORT))

    # Wait for user to type messages until user presses Ctrl-C, then quit.
    try:
        dummyInputField(socket)
    except KeyboardInterrupt:
        socket.close()
        print "\n[Closing socket and quitting.]"
