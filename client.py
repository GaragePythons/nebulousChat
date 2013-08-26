from enum import enum
from serializing import serialize, unserialize
import queries as q
import clientNetworking as n
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

def listener(sock):
    while True:
        n.receive(sock)


if __name__ == "__main__":
    # Connect to server.
    sendSocket = n.sendConnect((HOST, PORT))
    listenSocket = n.listenConnect((HOST, PORT))
    print (  "[Connected as " + n.clientAddress(sendSocket)[0]
           + ":" + str(n.clientAddress(sendSocket)[1]) + ".]")
    # Wait for user to type messages until user presses Ctrl-C, then quit.
    try:
        # dummyInputField(socket)
        senderThread = thread.start_new_thread(sender, (sendSocket,))
        listenerThread = thread.start_new_thread(listener, (listenSocket,))
    finally:
        sendSocket.close()
        listenSocket.close()
        print "\n[Closing socket and quitting.]"
