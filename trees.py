class MessageTree():
    def __init__(self, message):
        self.message = message
        self.children = []

    def traverse(self):
        yield self
        if self.children != []:
            for child in self.children:
                for x in child.traverse():
                    yield x

    def append(self, newMessageTree):
        parentID = newMessageTree.message.parentID
        for subTree in self.traverse():
            if parentID == subTree.message.ID:
                subTree.children.append(newMessageTree)
