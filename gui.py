from client import bootClient, timestamp
from parsing import hostTuple
import trees as t
import messages as m
import wx
import threading

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='nebulousChat')

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        dummyAddress = "123.45.67.89:9999"

        self.tree = wx.TreeCtrl(
            self.panel, wx.ID_ANY, wx.DefaultPosition, 
            (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|
            wx.TR_NO_LINES)
        self.root = self.tree.AddRoot("<" + dummyAddress + "> First ever nebC conversation!")

        self.graphNodes = {0: self.root}

        self.tree.Bind(
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

        topSizer.Add(self.tree, 1, wx.EXPAND)

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

    def onNickButtonPress(self, event, nickStr):
        nickDialog = wx.TextEntryDialog(
            self, "Enter your initials:", "Set initials")
        if nickDialog.ShowModal() == wx.ID_OK:
            nickStr = nickDialog.GetValue()
            self.nickButton.SetLabel("<" + nickStr + ">")
        nickDialog.Destroy()

    def onSelChanged(self, event):
        item = event.GetItem()

    def onEnter(self, event):
        msg = str(self.prompt.GetValue())
        self.client.messageIn.put(m.ChatMessage(
                0, self.client.ID, timestamp(), msg))
        self.prompt.Clear()

    def drawMessageTree(self, newMessageTree):
        print "Draw that!"
        for messageTree in newMessageTree.traverse():
            self.graphNodes[messageTree.message.ID] = \
                self.tree.AppendItem(
                    self.graphNodes[messageTree.message.parentID], 
                    messageTree.message.msg
                    )
        self.tree.ExpandAll()


    def listen(self, client):
        while True:
            # Wait until the client processes a message, then redraw the tree.
            newMessageTree = client.messageTreeOut.get()
            self.drawMessageTree(newMessageTree)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
