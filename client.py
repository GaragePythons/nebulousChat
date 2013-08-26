from serializing import serialize, unserialize
import queries as q
import clientNetworking as n
import server as s
import Queue
import threading
import time

HOST, PORT = "localhost", 9998

keywords = [("nick")]

def timestamp():
    return time.time()

def sender(sock):
    print "Running sender loop"
    try:
        while True:
            print "Waiting for raw input"
            messageString = raw_input()
            n.sendFromClient(
                serialize(q.Message(messageString, timestamp())), sock
                )
    except KeyboardInterrupt:
        signalToCloseSendSocket.put(1)

def listener(sock):
    while True:
        query = n.receive(sock)
        print "Received query"
        print query.MessageString


if __name__ == "__main__":
    # Connect to server.
    sendSocket = n.sendConnect((HOST, PORT))

    # Fudge so that the sender socket 
    # definitely gets opened first.
    # Things WILL break if two clients connect
    # within a second of each other.
    time.sleep(1)

    listenSocket = n.listenConnect((HOST, PORT))

    print (  "[Sending on   " + n.clientAddress(sendSocket)[0]
           + ":" + str(n.clientAddress(sendSocket)[1]) + ";\n"
           + " Listening on " + n.clientAddress(listenSocket)[0]
           + ":" + str(n.clientAddress(listenSocket)[1]) + ".]")


    signalToCloseSendSocket = Queue.Queue()
    senderThread = threading.Thread(
        target=sender, 
        args=(sendSocket,)
        )
    senderThread.daemon = True
    senderThread.start()

    signalToCloseListenSocket = Queue.Queue()
    listenerThread = threading.Thread(
        target=listener, 
        args=(listenSocket,)
        )
    listenerThread.daemon = True
    listenerThread.start()

    
    signalToCloseSendSocket.get()
    sendSocket.close()
    # listenSocket.close()
    print "\n[Closing socket and quitting.]"
