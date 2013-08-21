from serializing import serialize, unserialize
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        class ClientQuit(Exception):
            pass

        # There should be a way to move this definition outside of handle()...
        def getQuery():
            self.data = self.request.recv(1024)
            if self.data == '':
                print "[Client quit.]"
                raise ClientQuit
            self.request.sendall(self.data) # Send back the same data.
            return unserialize(self.data)

        # self.request is the TCP socket connected to the client.
        while True:
            try:
                self.query = getQuery()
            # Is this a good way to be using exceptions...?
            except ClientQuit:
                break

            # Work out what the client wants...
            print self.query.__class__.__name__

            # This is broken.
            self.server.globalQueriesList.append(self.query)
            print self.server.globalQueriesList.append(self.query)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999


    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.globalQueriesList = []
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    server.serve_forever()
