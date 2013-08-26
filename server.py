from serializing import serialize, unserialize
import Queue
import threading
import thread
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        queueList = self.server.queueList

        handleType = self.request.recv(1024)

        if handleType == "send":
            self.server.counter += 1
            clientID = self.server.counter
            self.request.sendall(serialize(clientID))

            print(  "[" + self.client_address[0] + " connected.]")

            queueList.append(Queue.Queue())

            while True:
                # self.request is the TCP socket connected to the client.
                data = self.request.recv(1024)
                self.request.sendall(data)
                
                if data == "":
                    break

                query = unserialize(data)
                print query.__class__.__name__
                server.queueForDistribution.put(query)
                
            print "[Client " + str(clientID) + " quit.]"

        else:
            assert handleType[0:6] == "listen"
            clientID = int(unserialize(handleType[6:]))

            while self.request.recv(1024) == "still here":
                self.request.sendall(serialize(
                    queueList[clientID - 1].get()
                    ))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.queueForDistribution = Queue.Queue()
    server.queueList = []
    server.counter = 0
    # server.globalQueriesList = []
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True

    def distributeQueries():
        while True:
            query = server.queueForDistribution.get()
            for queue in server.queueList:
                queue.put(query)

    distributionThread = threading.Thread(
        target=distributeQueries
        )
    distributionThread.daemon = True
    distributionThread.start()

    server.serve_forever()
