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

def sendFromClient(serializedData, sock):
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

def receiveToClient(sock):
    while True:
        received = sock.recv(1024)
        print received.messageString

def pullMessageList():
    pass

def clientAddress(sock):
    return sock.getsockname()
