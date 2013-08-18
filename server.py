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
        # self.request is the TCP socket connected to the client
        while(True):
            self.data = self.request.recv(1024)
            if(self.data == ''):
                print "[Client quit.]"
                break

            self.request.sendall(self.data) # Send back the same data.
            self.data = self.data.strip() # Strip _after_ checking for quit!
            print "{} wrote:".format(self.client_address[0])
            print self.data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Threading voodoo
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

    server.serve_forever()