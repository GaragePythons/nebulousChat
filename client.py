from serializing import serialize, unserialize
import messages as m
import clientNetworking as n
import Queue
import threading
import time
import sys

serverDetails = ("localhost", int(sys.argv[1]))

def timestamp():
    return time.time()

def speak(sock):
    while True:
        msg = raw_input(" > ")
        n.verifiedSend(
            serialize(m.ChatMessage(msg, timestamp())), sock
            )

def listen(sock):
    while True:
        n.send("still here", sock)
        message = unserialize(n.receive(sock))
        print message


if __name__ == "__main__":
    (speakSocket, serializedClientID) = n.openSpeakPort(serverDetails)
    # Sleep: fudge so that the sender socket 
    # definitely gets opened first.
    # Things WON'T break if two clients connect
    # within 0.1 seconds of each other.
    time.sleep(0.1)
    listenSocket = n.openListenPort(serverDetails, serializedClientID)
    clientID = unserialize(serializedClientID)

    print (  "[  Sending on " + n.address(speakSocket)[0]
           + ":" + str(n.address(speakSocket)[1]) + ";\n"
           + " Listening on " + n.address(listenSocket)[0]
           + ":" + str(n.address(listenSocket)[1]) 
           + ".\n You are client " + str(clientID) + ".            ]")

    speakThread = threading.Thread(
        target=speak, 
        args=(speakSocket,)
        )
    speakThread.daemon = True
    speakThread.start()

    signalToCloseListenSocket = Queue.Queue()
    listenThread = threading.Thread(
        target=listen, 
        args=(listenSocket,)
        )
    listenThread.daemon = True
    listenThread.start()

    try:
        time.sleep(99999999999999)
    finally:
        speakSocket.close()
        listenSocket.close()
        print "\n[Closed sockets; quitting.]"
