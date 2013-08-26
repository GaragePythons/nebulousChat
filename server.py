from serializing import serialize, unserialize
import Queue
import threading
import thread
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        queryQueues = self.server.queryQueues

        if self.request.recv(1024) == "send":

            self.server.counter += 1
            handlerID = self.server.counter

            print(  "[" + self.client_address[0] + ":"
                  + str(self.client_address[1]) + " connected.]")

            queryQueues.append(Queue.Queue())

            while True:
                # self.request is the TCP socket connected to the client.
                data = self.request.recv(1024)
                self.request.sendall(data)
                
                if data == "":
                    break

                query = unserialize(data)
                print query.__class__.__name__
                queryQueues.put(query)
                
            print "[Client quit.]"

        else:
            assert self.request.recv(1024) == "listen"

            handlerID = handlerID = self.server.counter

            print "[Client listening.]"
            print queryQueues[handlerID].get()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.queryQueues = []
    server.counter = 0
    # server.globalQueriesList = []
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True

    server.serve_forever()
