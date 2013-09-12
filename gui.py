from client import bootClient, timestamp
from parsing import hostTuple
import trees as t
import messages as m
import wx
import threading

class MainFrame(wx.Frame):

    def __init__(self):
        self.replyBranchID = 0
        wx.Frame.__init__(self, None, wx.ID_ANY, title='nebulousChat')

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        dummyAddress = "123.45.67.89:9999"

        self.graph = self.Graph(
            self.panel, wx.ID_ANY, wx.DefaultPosition, 
            (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|
            wx.TR_NO_LINES)
        self.root = self.graph.AddRoot("<" + dummyAddress + "> First ever nebC conversation!")

        self.graphNodes = {0: self.root}
        self.invGraphNodes = {self.root: 0}

        self.graph.Bind(
            wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, id=wx.ID_ANY)

        nickStr = "GP"

        self.nickButton = wx.Button(
            self.panel, wx.ID_ANY, "<" + nickStr + ">")
        self.nickButton.Bind(
            wx.EVT_BUTTON, 
            lambda event: self.onNickButtonPress(event, nickStr), 
            id=wx.ID_ANY)

        self.prompt = wx.TextCtrl(
            self.panel, style=wx.TE_PROCESS_ENTER)
        self.prompt.Bind(wx.EVT_TEXT_ENTER, self.onEnter)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        topSizer.Add(self.graph, 1, wx.EXPAND)

        bottomSizer.Add(self.nickButton, 0, wx.CENTRE)
        bottomSizer.Add(self.prompt, 1, wx.CENTRE)

        mainSizer.Add(topSizer, 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND)

        self.panel.SetSizer(mainSizer)
        topSizer.Fit(self)
        self.SetSize(wx.Size(800,600))

        def connect():
            connectDialog = wx.TextEntryDialog(self, "Enter host:", "Connect")
            connectDialog.SetValue("localhost:9999")
            if connectDialog.ShowModal() == wx.ID_OK:
                client = bootClient(hostTuple(connectDialog.GetValue()))
            connectDialog.Destroy()
            assert client
            return client

        self.client = connect()

        listenThread = threading.Thread(
            target = self.listen,
            args = (self.client,)
            )
        listenThread.daemon = True
        listenThread.start()

        self.prompt.SetFocus()

    class Graph(wx.TreeCtrl):
        pass

    def onNickButtonPress(self, event, nickStr):
        nickDialog = wx.TextEntryDialog(
            self, "Enter your initials:", "Set initials")
        if nickDialog.ShowModal() == wx.ID_OK:
            nickStr = nickDialog.GetValue()
            self.nickButton.SetLabel("<" + nickStr + ">")
        nickDialog.Destroy()

    def onSelChanged(self, event):
        self.replyBranchID = self.graph.GetPyData(event.GetItem())

    def onEnter(self, event):
        msg = str(self.prompt.GetValue())
        self.client.messageIn.put(m.ChatMessage(
                self.replyBranchID, self.client.ID, timestamp(), msg))
        self.prompt.Clear()

    def drawMessageTree(self, newMessageTree, isBaseMessageTree=False):
        if isBaseMessageTree:
            print "Drawing base: "
            self.graphRoot = self.graph.AddRoot("First ever nebC conversation!")
            for messageTree in newMessageTree.children:
                self.drawMessageTree(messageTree)
        else:
            for messageTree in newMessageTree.traverse():
                print "Drawing message " + messageTree.message.msg
                self.graphNodes[messageTree.message.ID] = \
                    self.graph.AppendItem(
                        self.graphNodes[messageTree.message.parentID], 
                        messageTree.message.msg
                        )
                # Associate the message ID with its node in the graph.
                self.graph.SetPyData(
                    self.graphNodes[messageTree.message.ID],
                    messageTree.message.ID
                    )
        self.graph.ExpandAll()
        self.graph.ScrollTo(self.graphNodes[messageTree.message.ID])


    def listen(self, client):
        self.drawMessageTree(client.baseMessageTree, True)
        while True:
            # Wait until the client processes a message, then redraw the graph.
            newMessageTree = client.messageTreeOut.get()
            print "Got to here..."
            self.drawMessageTree(newMessageTree)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
