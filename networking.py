import socket

RECV_SIZE = 16

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
    send(sock, "speak")
    serializedClientID = receive(sock)
    return (sock, serializedClientID)

def openListenPort((host, port), serializedClientID):
    sock = connect((host, port))
    send(sock, "listen" + serializedClientID)
    return sock

def send(sock, serializedMessage):
    lenSerializedMessage = len(serializedMessage)
    sock.sendall(str(len(serializedMessage)) + ':' + serializedMessage)

def receive(sock):
    serializedMessagePortion = sock.recv(RECV_SIZE)
    if serializedMessagePortion == "":
        return None
    while not ":" in serializedMessagePortion:
        serializedMessagePortion += sock.recv(RECV_SIZE)
    lenSerializedMessage = int(serializedMessagePortion.split(":", 1)[0])
    serializedMessagePortion = serializedMessagePortion.split(":", 1)[1]
    while len(serializedMessagePortion) != lenSerializedMessage:
        serializedMessagePortion += sock.recv(RECV_SIZE)
    return serializedMessagePortion

def address(sock):
    return sock.getsockname()
