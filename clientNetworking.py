import socket

def connect((HOST, PORT)):
    try:
        sock = socket.socket()
        sock.bind(('', 0))
        sock = socket.create_connection((HOST, PORT))
        return sock
    except:
        print "[Connecting failed.]"
        raise

def sendConnect((HOST, PORT)):
    sock = connect((HOST, PORT))
    sock.sendall("send")
    serializedClientID = sock.recv(1024)
    return (sock, serializedClientID)

def listenConnect((HOST, PORT), serializedClientID):
    sock = connect((HOST, PORT))
    sock.sendall("listen" + serializedClientID)
    return sock

def sendString(string, sock):
    sock.sendall(string)

def receiveString(sock):
    return sock.recv(1024)

def verifiedSend(serializedData, sock):
    try:
        sock.sendall(serializedData)
    except:
        print "[Could not send data.]"

    try:
        received = sock.recv(1024)
    except:
        print "[Confirmation of receipt not received from server.]"
        raise

    if received != serializedData:
        print "[Data was mangled between client and server!]"

def clientAddress(sock):
    return sock.getsockname()
