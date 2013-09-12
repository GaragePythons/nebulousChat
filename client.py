from serializing import serialize, unserialize
import networking as n
import messages as m
import trees
import Queue
import threading
import time
import sys

def timestamp():
    return time.time()

def speak(sock, client):
    while True:
        newMessage = client.messageIn.get()
        n.send(sock, serialize(newMessage))

def listen(sock, client):
    while True:
        n.send(sock, "still here")
        newMessage = unserialize(n.receive(sock))
        newMessageTree = trees.MessageTree(newMessage)
        client.baseMessageTree.append(newMessageTree)
        client.messageTreeOut.put(newMessageTree)

class Client():
    pass

def bootClient(SERVER_DETAILS):
    client = Client()
    (client.speakSocket, serializedClientID) = n.openSpeakPort(SERVER_DETAILS)
    # Sleep: fudge so that the sender socket 
    # definitely gets opened first.
    # Things WON'T break if two clients connect
    # within 0.1 seconds of each other.
    time.sleep(0.1)
    client.listenSocket = n.openListenPort(SERVER_DETAILS, serializedClientID)
    client.ID = unserialize(serializedClientID)

    client.baseMessageTree = trees.MessageTree(m.Message(None, 0, None, "Conversation"))
    client.baseMessageTree.message.ID = 0

    # "In" = "in from server"; "Out" = "out to GUI"
    client.messageIn = Queue.Queue()
    client.messageTreeOut = Queue.Queue()

    speakThread = threading.Thread(
        target=speak, 
        args=(client.speakSocket, client)
        )
    speakThread.daemon = True
    speakThread.start()

    listenThread = threading.Thread(
        target=listen, 
        args=(client.listenSocket, client)
        )
    listenThread.daemon = True
    listenThread.start()

    return client


if __name__ == "__main__":
    SERVER_DETAILS = (sys.argv[1], int(sys.argv[2]))
    client = bootClient(SERVER_DETAILS)

    print (  "[  Sending on " + n.address(client.speakSocket)[0]
           + ":" + str(n.address(client.speakSocket)[1]) + ";\n"
           + " Listening on " + n.address(client.listenSocket)[0]
           + ":" + str(n.address(client.listenSocket)[1]) 
           + ".\n You are client " + str(client.ID) + ".            ]")

    try:
        while True:
            msg = raw_input()
            client.messageIn.put(m.ChatMessage(
                0, client.ID, timestamp(), msg))
    finally:
        client.speakSocket.close()
        client.listenSocket.close()
        print "[Closed sockets; quitting.]"
