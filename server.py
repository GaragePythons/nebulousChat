from serializing import serialize, unserialize
from networking import verifiedSend, hearVerifiedSend
import messages as m
import trees
import signal
import Queue
import threading
import SocketServer
import time
import sys

def assignID(message):
    pass

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # handle() handles incoming connections 
    # whether they be speakers or listeners.
    def handle(self):

        # socketType refers to whether the socket is a speaker 
        # or listener from the _client's_ point of view.
        socketType = self.request.recv(1024)

        if socketType == "speak":

            # Should use a lock or something to ensure the following 
            # two lines get executed by a single thread at a time.
            clientIDLock.acquire()
            clientID = server.clientIDCounter
            server.clientIDCounter += 1
            clientIDLock.release()

            # Tell the client its ID.
            self.request.sendall(serialize(clientID))

            print(  "[" + self.client_address[0] + " connected as client "
                  + str(clientID) + ".]")
            # Create a queue corresponding to this client.
            server.messages.append(Queue.Queue())

            while True:
                serializedMessage = hearVerifiedSend(self.request)
                if serializedMessage:
                    message = unserialize(serializedMessage)
                    print message.__class__.__name__
                    server.distributionQueue.put(message)
                    assignID(message)
                    # Tell the server the messageID.
                    # Put the message in the baseMessageTree.
                else:
                    break
                
            print "[Client " + str(clientID) + " quit.]"

        else:
            assert socketType[0:6] == "listen"
            clientID = int(unserialize(socketType[6:]))

            # While the client is still listening...
            while self.request.recv(1024) == "still here":
                # ...send a message from the queue 
                # corresponding to this client.
                self.request.sendall(serialize(
                    server.messages[clientID].get()
                    ))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", int(sys.argv[1])

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.distributionQueue = Queue.Queue()
    server.messages = []
    clientIDLock = threading.Lock()
    server.clientIDCounter = 0
    baseMessageTree = trees.MessageTree(None)

    def distributeMessage():
        while True:
            message = server.distributionQueue.get()
            for queue in server.messages:
                queue.put(message)

    distributionThread = threading.Thread(
        target=distributeMessage
        )
    distributionThread.daemon = True

    distributionThread.start()

    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True
    serverThread.start()

    signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
    signal.pause()
