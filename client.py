from serializing import serialize, unserialize
import queries as q
import clientNetworking as n
import Queue
import threading
import time

connectInfos = ("localhost", 9999)

def timestamp():
    return time.time()

def sender(sock):
    try:
        while True:
            messageString = raw_input()
            n.verifiedSend(
                serialize(q.Message(messageString, timestamp())), sock
                )
    except KeyboardInterrupt:
        signalToCloseSendSocket.put(1)

def listener(sock):
    while True:
        n.sendString("still here", sock)
        query = unserialize(n.receiveString(sock))
        print query.messageString


if __name__ == "__main__":
    sendSocket = n.sendConnect(connectInfos)
    # Sleep: fudge so that the sender socket 
    # definitely gets opened first.
    # Things WILL break if two clients connect
    # within a second of each other.
    time.sleep(1)
    listenSocket = n.listenConnect(connectInfos)

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
    listenSocket.close()
    print "\n[Closing socket and quitting.]"
