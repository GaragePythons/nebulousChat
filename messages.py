class Message():
    def __init__(self, parentID, clientID, timestamp, txt):
        self.parentID = parentID
        self.clientID = clientID
        self.timestamp = timestamp
        self.txt = txt
        # messages also get given an ID by the server.

    def __str__(self):
        return self.txt

class ChatMessage(Message):
    pass

class SetNick(Message):
    pass
