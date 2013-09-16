from client import bootClient, timestamp
from parsing import hostTuple
import trees as t
import messages as m
import wx
import threading
import time

class MainFrame(wx.Frame):

    def __init__(self):
        self.replyBranchID = 0
        wx.Frame.__init__(self, None, wx.ID_ANY, title='nebulousChat')

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.graph = self.Graph(
            self.panel, wx.ID_ANY, wx.DefaultPosition, 
            (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|
            wx.TR_NO_LINES)

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
        self.prompt.Bind(wx.EVT_KILL_FOCUS, self.onLoseFocus)

        self.multilineInputButton = wx.Button(
            self.panel, wx.ID_ANY, "Multi-line input...")
        self.multilineInputButton.Bind(wx.EVT_BUTTON,
            lambda event: self.onMultilineInputButtonPress(event)
            )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        topSizer.Add(self.graph, 1, wx.EXPAND)

        bottomSizer.Add(self.nickButton, 0, wx.CENTRE)
        bottomSizer.Add(self.prompt, 1, wx.CENTRE)
        bottomSizer.Add(self.multilineInputButton, 0, wx.CENTRE)

        mainSizer.Add(topSizer, 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND)

        self.panel.SetSizer(mainSizer)
        topSizer.Fit(self)
        self.SetSize(wx.Size(600,600))

        def connect():
            connectDialog = wx.TextEntryDialog(self, "Enter host:", "Connect")
            connectDialog.SetValue("localhost:9999")
            if connectDialog.ShowModal() == wx.ID_OK:
                client = bootClient(hostTuple(connectDialog.GetValue()))
            connectDialog.Destroy()
            assert client
            return client

        self.client = connect()

        self.root = self.graph.AddRoot(str(self.client.baseMessageTree.message))
        self.graph.SetPyData(self.root, 0)

        self.graphNodes = {0: self.root}

        self.graph.Bind(
            wx.EVT_TREE_ITEM_ACTIVATED, self.onSelChanged, id=wx.ID_ANY)

        listenThread = threading.Thread(
            target = self.listen,
            args = (self.client,)
            )
        listenThread.daemon = True
        listenThread.start()

        self.prompt.SetFocus()
        self.prompt.Bind(wx.EVT_SET_FOCUS, self.onFocus)

    class TextEntryDialog(wx.Dialog):
        def __init__(self, parent, title, caption):
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
            super(type(self), self).__init__(parent, -1, title, style=style)
            text = wx.StaticText(self, -1, caption)
            input = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
            input.SetInitialSize((400, 300))
            buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(text, 0, wx.ALL, 5)
            sizer.Add(input, 1, wx.EXPAND|wx.ALL, 5)
            sizer.Add(buttons, 0, wx.EXPAND|wx.ALL, 5)
            self.SetSizerAndFit(sizer)
            self.input = input
        def SetValue(self, value):
            self.input.SetValue(value)
        def GetValue(self):
            return self.input.GetValue()
        def SetFocus(self):
            self.input.SetSelection(-1,-1)
            self.input.SetFocus()

    class Graph(wx.TreeCtrl):
        pass

    def onNickButtonPress(self, event, nickStr):
        nickDialog = wx.TextEntryDialog(
            self, "Enter your initials:", "Set initials")
        if nickDialog.ShowModal() == wx.ID_OK:
            nickStr = nickDialog.GetValue()
            self.nickButton.SetLabel("<" + nickStr + ">")
        nickDialog.Destroy()
        self.prompt.SetFocus()

    def onMultilineInputButtonPress(self, event):
        multilineInputDialog = self.TextEntryDialog(
            self, "Multi-line input", ""
            )
        multilineInputDialog.SetValue(self.prompt.GetValue())
        multilineInputDialog.SetFocus()
        if multilineInputDialog.ShowModal() == wx.ID_OK:
            self.prompt.SetValue(multilineInputDialog.GetValue())
        multilineInputDialog.Destroy()
        self.prompt.SetFocus()

    def onSelChanged(self, event):
        self.replyBranchID = self.graph.GetPyData(event.GetItem())
        self.setFocusToPrompt()

    def setFocusToPrompt(self):
        self.prompt.SetFocus()

    def onFocus(self, event):
        pass

    def onLoseFocus(self, event):
        pass

    def onEnter(self, event):
        txt = str(self.prompt.GetValue())
        self.client.messageIn.put(m.ChatMessage(
                self.replyBranchID, self.client.ID, timestamp(), txt))
        self.prompt.Clear()

    def drawMessageTree(self, newMessageTree, isBaseMessageTree=False):
        if isBaseMessageTree:
            print "Drawing base"
            for messageTree in newMessageTree.children:
                self.drawMessageTree(messageTree)
        else:
            for messageTree in newMessageTree.traverse():
                print (  "Drawing message from client " 
                       + str(messageTree.message.clientID) + ": "
                       + str(messageTree.message))
                self.graphNodes[messageTree.message.ID] = \
                    self.graph.AppendItem(
                        self.graphNodes[messageTree.message.parentID], 
                        str(messageTree.message)
                        )
                if "\n" in str(messageTree.message):
                    print "Setting fixed font on " + str(messageTree.message)
                    self.graph.SetItemFont(
                        self.graphNodes[messageTree.message.ID],
                        wx.Font(
                            10,
                            wx.FONTFAMILY_MODERN,
                            1,
                            self.graph.GetItemFont(self.root).GetWeight()
                            )
                        )
                # Associate the message ID with its node in the graph.
                self.graph.SetPyData(
                    self.graphNodes[messageTree.message.ID],
                    messageTree.message.ID
                    )
            self.graph.ExpandAll()
            self.graph.ScrollTo(self.graphNodes[newMessageTree.message.ID])


    def listen(self, client):
        self.drawMessageTree(client.baseMessageTree, True)
        while True:
            # Wait until the client processes a message, then redraw the graph.
            newMessageTree = client.messageTreeOut.get()
            self.drawMessageTree(newMessageTree)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
