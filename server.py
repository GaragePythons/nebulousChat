import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
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

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
