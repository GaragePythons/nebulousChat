class Query():
    pass

class Message(Query):
    def __init__(self, messageString, timestamp):
        self.messageString = messageString
        self.timestamp = timestamp

class SetNick(Query):
    pass
