class Message():
    def __init__(self, parentID, clientID, timestamp, txt):
        self.parentID = parentID
        self.clientID = clientID
        self.timestamp = timestamp
        self.txt = txt
        # messages also get given an ID by the server.

class ChatMessage(Message):
    def __str__(self):
        return str(self.ID) + " > " + self.txt

    def printWithContext():
        print "> " + self.parent + ";\n" + self;

class SetNick(Message):
    def __str__():
        return self.str
