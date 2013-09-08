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
    return sock.recv(1024)

def verifiedSend(sock, serializedData):
    try:
        sock.sendall(serializedData)
    except:
        print "[Could not send data.]"

    try:
        received = sock.recv(1024)
    except:
        print "[Confirmation of receipt not received from server.]"

    if received != serializedData:
        print "[Data was mangled between client and server!]"

def hearVerifiedSend(sock):
    serializedMessage = sock.recv(1024)
    
    if serializedMessage == "":
        return None
    else:
        sock.sendall(serializedMessage)
        return serializedMessage

def address(sock):
    return sock.getsockname()
