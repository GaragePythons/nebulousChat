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
            print "HandlerID of send is " + str(self.server.counter)
            handlerID = self.server.counter

            print(  "[" + self.client_address[0] + ":"
                  + str(self.client_address[1]) + " connected.]")

            queueList.append(Queue.Queue())
            print "Appended a Queue to queueList"

            while True:
                # self.request is the TCP socket connected to the client.
                data = self.request.recv(1024)
                self.request.sendall(data)
                
                if data == "":
                    break

                query = unserialize(data)
                print query.__class__.__name__
                server.queueForDistribution.put(query)
                
            print "[Client quit.]"

        else:
            assert handleType == "listen"
            handlerID = self.server.counter
            print "handlerID of listen is " + str(handlerID)

            while self.request.recv(1024) == "still here":
                print "Waiting for query"
                query = queueList[handlerID - 1].get()
                print "Got query"
                self.request.sendall(serialize(query))
                print "!"


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.queueForDistribution = Queue.Queue()
    server.queueList = []
    server.counter = 0
    # server.globalQueriesList = []
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True

    def distributeQuery():
        while True:
            query = server.queueForDistribution.get()
            print "Distributing query"
            for queue in server.queueList:
                queue.put(query)

    distributionThread = threading.Thread(
        target=distributeQuery
        )
    distributionThread.daemon = True
    distributionThread.start()

    server.serve_forever()
