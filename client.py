from enum import enum
import parsing
import networking

HOST, PORT = "localhost", 9999

messageTypes = enum('chatLine', 'setNick')
keywordTuples = [None]*2  # Initialise list of keyword tuples.
keywordTuples[messageTypes.setNick] = ('nick', 'setnick')

def parse(rawInput):
    if(rawInput == ''):
        print "[Please do not feed me empty strings!]"
    messageType = parsing.findMessageType(rawInput, 
                                          keywordTuples, 
                                          messageTypes.chatLine)
    if(messageType != messageTypes.chatLine):
        string = parsing.stripKeyword(rawInput)
    else:
        string = rawInput
    return (messageType, string)

def serialize(parsedInput):
    return parsedInput[1]

# Connect to server.
socket = networking.connect((HOST, PORT))

# Wait for user to type messages until user presses Ctrl-C, then quit.
try:
    while True:
        networking.send(serialize(parse(raw_input())), socket)
except KeyboardInterrupt:
    socket.close()
    print "\n[Closing socket and quitting.]"
