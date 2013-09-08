from serializing import serialize, unserialize
import networking as n
import messages as m
import trees
import Queue
import threading
import time
import sys

SERVER_DETAILS = (sys.argv[1], int(sys.argv[2]))

def timestamp():
    return time.time()

def speak(sock, message, clientID):
    while True:
        newMessage = message.get()
        n.send(sock, serialize(newMessage))
        newMessage.ID = unserialize(n.receive(sock))
        newMessageTree = trees.MessageTree(newMessage)
        baseMessageTree.append(newMessageTree)


def listen(sock):
    while True:
        n.send(sock, "still here")
        message = unserialize(n.receive(sock))
        print message


if __name__ == "__main__":
    (speakSocket, serializedClientID) = n.openSpeakPort(SERVER_DETAILS)
    # Sleep: fudge so that the sender socket 
    # definitely gets opened first.
    # Things WON'T break if two clients connect
    # within 0.1 seconds of each other.
    time.sleep(0.1)
    listenSocket = n.openListenPort(SERVER_DETAILS, serializedClientID)
    clientID = unserialize(serializedClientID)

    print (  "[  Sending on " + n.address(speakSocket)[0]
           + ":" + str(n.address(speakSocket)[1]) + ";\n"
           + " Listening on " + n.address(listenSocket)[0]
           + ":" + str(n.address(listenSocket)[1]) 
           + ".\n You are client " + str(clientID) + ".            ]")

    baseMessageTree = trees.MessageTree(m.Message(None, 0, None, None))
    baseMessageTree.message.ID = 0

    message = Queue.Queue()

    speakThread = threading.Thread(
        target=speak, 
        args=(speakSocket, message, clientID)
        )
    speakThread.daemon = True
    speakThread.start()

    listenThread = threading.Thread(
        target=listen, 
        args=(listenSocket,)
        )
    listenThread.daemon = True
    listenThread.start()

    try:
        while True:
            msg = raw_input()
            message.put(m.ChatMessage(0, clientID, timestamp(), msg))
    finally:
        speakSocket.close()
        listenSocket.close()
        print "[Closed sockets; quitting.]"
