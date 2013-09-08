import socket

def connect((host, port)):
    try:
        sock = socket.socket()
        sock.bind(('', 0))
        sock = socket.create_connection((host, port))
        return sock
    except:
        print "[Connecting failed.]"
        raise

def openSpeakPort((host, port)):
    sock = connect((host, port))
    sock.sendall("speak")
    serializedClientID = sock.recv(1024)
    return (sock, serializedClientID)

def openListenPort((host, port), serializedClientID):
    sock = connect((host, port))
    sock.sendall("listen" + serializedClientID)
    return sock

def send(sock, string):
    sock.sendall(string)

def receive(sock):
    serializedMessage = sock.recv(1024)
    if serializedMessage == "":
        return None
    else:
        return serializedMessage

def address(sock):
    return sock.getsockname()
