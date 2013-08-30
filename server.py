from serializing import serialize, unserialize
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
        socketType = self.request.recv(1024)

        if socketType == "speak":
            # This is potentially bad if two clients 
            # join at exactly the same time.
            clientID = server.clientIDCounter
            server.clientIDCounter += 1
            # Tell the client its ID.
            self.request.sendall(serialize(clientID))

            print(  "[" + self.client_address[0] + " connected as client "
                  + str(clientID) + ".]")

            # Create a queue corresponding to this client.
            server.messages.append(Queue.Queue())

            # Listen for verifiedSend() from client.
            while True:
                serializedMessage = self.request.recv(1024)
                self.request.sendall(serializedMessage)
                
                if serializedMessage == "":
                    break

                message = unserialize(serializedMessage)
                print message.__class__.__name__
                server.distributionQueue.put(message)
                
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
    server.clientIDCounter = 0

    def distributeMessages():
        while True:
            message = server.distributionQueue.get()
            for queue in server.messages:
                queue.put(message)

    distributionThread = threading.Thread(
        target=distributeMessages
        )
    distributionThread.daemon = True

    distributionThread.start()

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(99999999999999)
