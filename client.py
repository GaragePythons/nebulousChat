from enum import enum
from serializing import serialize, unserialize
import queries as q
import networking as n
import server as s
import thread
import time

HOST, PORT = "localhost", 9998

keywords = [("nick")]

def timestamp():
    return time.time()

def sender(sock):
    while True:
        messageString = raw_input()
        n.sendFromClient(serialize(q.Message(messageString, timestamp())), sock)

def receiver(sock):
    while True:
        n.receiveToClient(sock)


if __name__ == "__main__":
    # Connect to server.
    sendSocket = n.connect((HOST, PORT))
    receiveSocket = n.connect((HOST, PORT))
    print (  "[Connected as " + n.clientAddress(socket)[0]
           + ":" + str(n.clientAddress(socket)[1]) + ".]")
    # Wait for user to type messages until user presses Ctrl-C, then quit.
    try:
        # dummyInputField(socket)
        senderThread = thread.start_new_thread(sender, (sendSocket))
        receiverThread = thread.start_new_thread(receiver, (receiveSocket))
    finally:
        socket.close()
        print "\n[Closing socket and quitting.]"
