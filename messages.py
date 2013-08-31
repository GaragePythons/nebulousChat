class Message():
    def __init__(self, msg, timestamp):
        self.msg = msg
        self.timestamp = timestamp

class ChatMessage(Message):
    """ChatMessages have children but not parents - 
    at least, not explicitly."""

    def __init__(self, parentID, clientID, timestamp, msg):
        self.parentID = parentID
        self.clientID = clientID
        self.timestamp = timestamp
        self.msg = msg

    def __str__(self):
        return self.msg

    def printWithContext():
        print "> " + self.parent + ";\n" + self;

class SetNick(Message):
    def __str__():
        return self.str
