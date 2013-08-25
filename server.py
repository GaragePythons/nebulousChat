from serializing import serialize, unserialize
import Queue
import threading
import thread
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        def getConnectionType():
            pass
    
        queries = self.server.queries
    
        print(  "[" + self.client_address[0] + ":"
              + str(self.client_address[1]) + " connected.]")

        while True:
            # self.request is the TCP socket connected to the client.
            data = self.request.recv(1024)
            self.request.sendall(data)
            
            if data == "":
                break

            query = unserialize(data)
            print query.__class__.__name__
            queries.put(query)
            
        print "[Client quit.]"

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.queries = Queue.Queue()
    # server.globalQueriesList = []
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True

    server.serve_forever()
