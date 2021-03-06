from serializing import serialize, unserialize
import networking as n
import messages as m
import trees
import signal
import Queue
import threading
import SocketServer
import time
import sys

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    # handle() handles incoming connections 
    # whether they be speakers or listeners.
    def handle(self):

        # socketType refers to whether the socket is a speaker 
        # or listener from the _client's_ point of view.
        socketType = n.receive(self.request)

        if socketType == "speak":
            server.clientIDLock.acquire()
            clientID = server.clientIDCounter
            server.clientIDCounter += 1
            server.clientIDLock.release()

            # Tell the client its ID.
            n.send(self.request, serialize(clientID))

            print(  "[" + self.client_address[0] + " connected as client "
                  + str(clientID) + ".]")
            # Create a queue corresponding to this client.
            server.messages.append(Queue.Queue())

            while True:
                serializedMessage = n.receive(self.request)
                if serializedMessage:
                    message = unserialize(serializedMessage)
                    print (  "[" + message.__class__.__name__ 
                           + ": " + str(message) + "]")
                    assignID(message)
                    server.distributionQueue.put(message)
                    newMessageTree = trees.MessageTree(message)
                    server.baseMessageTree.append(newMessageTree)
                else:
                    break
                
            print "[Client " + str(clientID) + " quit.]"

        else:
            assert socketType[0:6] == "listen"
            clientID = int(unserialize(socketType[6:]))

            n.send(self.request, serialize(server.baseMessageTree))

            # While the client is still listening...
            while n.receive(self.request) == "still here":
                # ...send a message from the queue 
                # corresponding to this client.
                n.send(self.request, serialize(
                    server.messages[clientID].get()
                    ))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    pass


if __name__ == "__main__":
    HOST, PORT = "", int(sys.argv[1])

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.distributionQueue = Queue.Queue()
    server.messages = []
    server.clientIDLock = threading.Lock()
    server.clientIDCounter = 0
    server.messageIDLock = threading.Lock()
    server.messageIDCounter = 0
    server.baseMessageTree = trees.MessageTree(
        m.Message(None, None, None, "My conversation subject"))
    server.baseMessageTree.message.ID = 0

    def assignID(message):
        server.messageIDLock.acquire()
        server.messageIDCounter += 1
        message.ID = server.messageIDCounter
        server.messageIDLock.release()

    def distributeMessage():
        while True:
            message = server.distributionQueue.get()
            for queue in server.messages:
                queue.put(message)

    def writeMessageTreeToFile(filename):
        file = open(filename, "w")
        file.write(serialize(server.baseMessageTree))
        file.close()

    def writeOnRequest():
        while True:
            if raw_input() == "write":
                writeMessageTreeToFile(".messages")
                print "[Wrote entire message tree to .messages.]"
            else:
                print (  "[Please enter a valid command. " 
                       + "Currently the only valid command is \"write\".]")

    def initializeServerControl():
        try:
            with open(".messages", "r") as file:
                print (  "[File exists at .messages. "
                       + "Attempt to load the message tree? (y/n)]")
                def queryForImport():
                    response = raw_input()
                    if response == "y":
                        server.baseMessageTree = unserialize(file.read())
                        print "[Read message tree from .messages; proceeding.]"
                    elif response == "n":
                        print "[Proceeding without importing from .messages.]"
                    else:
                        print "[y/n]"
                        queryForImport()
                queryForImport()
                # The with statement closes the file.
        except IOError:
            print "[Nothing found at .messages; proceeding.]"

    initializeServerControl()

    serverControlThread = threading.Thread(
        target=writeOnRequest
        )
    serverControlThread.daemon = True
    serverControlThread.start()

    distributionThread = threading.Thread(
        target=distributeMessage
        )
    distributionThread.daemon = True
    distributionThread.start()

    serverThread = threading.Thread(
        target=server.serve_forever
        )
    serverThread.daemon = True
    print "[Listening...]"
    serverThread.start()

    signal.signal(signal.SIGINT, lambda signal, frame: sys.exit(0))
    signal.pause()
