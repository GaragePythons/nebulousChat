import socket

def connect((HOST, PORT)):
    try:
        sock = socket.create_connection((HOST, PORT))
        return sock
    except:
        print "[Connecting failed.]"
        raise

def send(serializedData, sock):
    try:
        sock.sendall(serializedData)
    except:
        print "[Could not send data.]"

    try:
        received = sock.recv(1024)
    except:
        print "[Confirmation of receipt not received from server.]"
        raise

    if (received != serializedData):
        print "[Data was mangled between client and server!]"
