class Message():
    def __init__(self, str, timestamp):
        self.str = str
        self.timestamp = timestamp

class ChatMessage(Message):
    def __str__(self):
        return self.str

class SetNick(Message):
    def __str__():
        return self.str
