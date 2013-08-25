from serializing import serialize, unserialize
import Queue
import threading
import thread
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        
        class ClientQuit(Exception):
            pass

        def getConnectionType():
            pass

        # There should be a way to move this definition outside of handle()...
        def getQueries():
            while True: 
                self.data = self.request.recv(1024)
                if self.data == '':
                    print "[Client quit.]"
                    raise ClientQuit
                self.request.sendall(self.data) # Send back the same data.
                return unserialize(self.data)

        def sendQueries():
            while True:
                self.server.queryQueue.get()


        print(  "[" + self.client_address[0] + ":"
              + str(self.client_address[1]) + " connected.]")

        # self.request is the TCP socket connected to the client.
        while True:
            # Wait for EITHER client query OR news from another handle().
            try:
                self.query = getQuery()
            # Is this a good way to be using exceptions...?
            except ClientQuit:
                break

            # Work out what the client wants...
            print self.query.__class__.__name__

            # This is broken.
            self.server.queryQueue.put(self.query)
            # print self.server.globalQueriesList.append(self.query)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998


    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.queryQueue = Queue.Queue()
    # server.globalQueriesList = []
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True

    server.serve_forever()
