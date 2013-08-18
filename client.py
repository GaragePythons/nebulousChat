import socket
import sys
from customEnum import enum

HOST, PORT = "localhost", 9999

messageType = enum('chatLine', 'nick')

def send(serializedData):
    try:
        try:
            sock = socket.create_connection((HOST, PORT))
        except:
            print "[Connecting failed.]"
            raise  # Don't close the socket, because it was never opened (hopefully?).

        try:
            try:
                sock.sendall(serializedData)
            except:
                print "[Could not send data.]"
                raise

            try:
                received = sock.recv(1024)
            except:
                print "[Confirmation of receipt not received from server.]"
                raise

            if (received != serializedData):
                print "[Data was mangled between client and server.]"
                raise

        finally:
            sock.close()
            print "[Closed socket.]"

    except:
        pass

def parse(rawInput):
    return rawInput

def serialize(parsedInput):
    return parsedInput

# Wait for user to type messages until user presses Ctrl-C, then quit.
try:
    while(True):
        send(serialize(parse(raw_input())))
except KeyboardInterrupt:
    print "\n[Quitting.]"
