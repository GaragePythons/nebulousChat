from client import bootClient, timestamp
from parsing import hostTuple
import trees as t
import messages as m
import wx
import threading
import time

class MainFrame(wx.Frame):

    def __init__(self):

# FONTS

        self.fixed = wx.Font(
            10,                     # size
            wx.FONTFAMILY_MODERN,   # family
            wx.NORMAL,              # style (bold, etc.)
            wx.NORMAL               # weight
            )

        # Not currently in use.
        self.sans = wx.Font(
            10,                     # size
            wx.FONTFAMILY_DEFAULT,  # family
            wx.NORMAL,              # style (bold, etc.)
            wx.NORMAL               # weight
            )

# INITIALIZE GUI

        wx.Frame.__init__(self, None, wx.ID_ANY, title='nebulousChat')

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        self.graph = self.Graph(
            self.panel, wx.ID_ANY, wx.DefaultPosition, 
            (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|
            wx.TR_ROW_LINES)

        nickStr = "GP"
        
        self.twoCharTuples = ((chr(x), chr(y)) 
            for x in xrange(ord("1"), ord("~")+1) 
            for y in xrange(ord("1"), ord("~")+1)
            )
        self.twoCharStrings = {}
        self.replyBranchID = 0

        self.nickButton = wx.Button(
            self.panel, wx.ID_ANY, "<" + nickStr + ">")
        self.nickButton.Bind(
            wx.EVT_BUTTON, 
            lambda event: self.onNickButtonPress(event, nickStr), 
            id=wx.ID_ANY)

        self.prompt = wx.TextCtrl(
            self.panel, style=wx.TE_PROCESS_ENTER)
        self.prompt.Bind(wx.EVT_TEXT_ENTER, self.onPromptEnter)
        self.prompt.Bind(wx.EVT_KILL_FOCUS, self.onPromptLoseFocus)

        self.multilineInputButton = wx.Button(
            self.panel, wx.ID_ANY, "Multi-line input...")
        self.multilineInputButton.Bind(wx.EVT_BUTTON,
            lambda event: self.onMultilineInputButtonPress(event)
            )

        self.branchSelector = wx.TextCtrl(
            self.panel, style=wx.TE_PROCESS_ENTER)
        self.branchSelector.SetFont(self.fixed)
        self.branchSelector.Bind(wx.EVT_TEXT_ENTER, self.onBranchSelectorEnter)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        topSizer.Add(self.graph, 1, wx.EXPAND)

        bottomSizer.Add(self.nickButton, 0, wx.CENTRE)
        bottomSizer.Add(self.prompt, 1, wx.CENTRE)
        bottomSizer.Add(self.multilineInputButton, 0, wx.CENTRE)
        bottomSizer.Add(self.branchSelector, 0, wx.CENTRE)

        mainSizer.Add(topSizer, 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND)

        self.panel.SetSizer(mainSizer)
        topSizer.Fit(self)
        self.SetSize(wx.Size(600,600))


# CONNECT AND SET UP GRAPH DRAWING

        def connect():
            connectDialog = wx.TextEntryDialog(self, "Enter host:", "Connect")
            connectDialog.SetValue("localhost:9999")
            if connectDialog.ShowModal() == wx.ID_OK:
                client = bootClient(hostTuple(connectDialog.GetValue()))
            connectDialog.Destroy()
            assert client
            return client

        self.client = connect()

        self.nicks = {
            None: "Server",
            0: "Alfie", 
            1: "Bobby",
            2: "Chop-chop",
            3: "Danny",
            4: "Errol",
            5: "Flynn"
        }

        self.graph.Bind(
            wx.EVT_TREE_ITEM_ACTIVATED, self.onSelChanged, id=wx.ID_ANY)

        listenThread = threading.Thread(
            target = self.listen,
            args = (self.client,)
            )
        listenThread.daemon = True
        listenThread.start()

        self.prompt.SetFocus()
        self.prompt.Bind(wx.EVT_SET_FOCUS, self.onPromptGainFocus)


    # Custom multi-line text-entry.
    class TextEntryDialog(wx.Dialog):
        def __init__(self, parent, title, caption):
            style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
            # No idea what's going on here.
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

    # Graph: visible stuff. MessageTree: data structure.
    class Graph(wx.TreeCtrl):
        pass


# BUTTON PRESS FUNCTIONS

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


# PROMPT FUNCTIONS

    def setFocusToPrompt(self):
        self.prompt.SetFocus()

    def onPromptGainFocus(self, event):
        pass

    def onPromptLoseFocus(self, event):
        pass

    def onPromptEnter(self, event):
        txt = str(self.prompt.GetValue())
        self.client.messageIn.put(m.ChatMessage(
                self.replyBranchID, self.client.ID, timestamp(), txt))
        self.prompt.Clear()


# BRANCH SELECTOR FUNCTIONS

    def onBranchSelectorEnter(self, event):
        newBranchTwoCharString = self.branchSelector.GetValue()
        self.branchSelector.SetValue(  "branch " 
                                     + self.twoCharStrings[self.replyBranchID])
        self.replyBranchIDDict = \
            dict((v,k) for k,v in self.twoCharStrings.items())
        try:
            self.replyBranchID = self.replyBranchIDDict[newBranchTwoCharString]
        except KeyError:
            print "Invalid key; reply branch unchanged."
        finally:
            self.reprintBranchSelectorText()
            self.setFocusToPrompt()

    def reprintBranchSelectorText(self):
        self.branchSelector.SetValue(  "branch " 
                                     + self.twoCharStrings[self.replyBranchID])
        # Piggyback on this function to select the correct message in graph.
        self.graph.SelectItem(self.graphNodes[self.replyBranchID])
        # Also scroll to where the user probably wants to be.
        self.scrollToBottomOfBranch(self.replyBranchID)


# GRAPH ACTION FUNCTIONS

    def onSelChanged(self, event):
        self.replyBranchID = self.graph.GetPyData(event.GetItem())
        self.reprintBranchSelectorText()
        self.setFocusToPrompt()

    def scrollToBottomOfBranch(self, branchID):
        pass

    def drawMessageTree(self, newMessageTree, isBaseMessageTree=False):
        if isBaseMessageTree:
            print "Drawing base"
            self.root = self.graph.AddRoot("Server<" 
                + self.twoCharStrings[0] + ">  "
                + str(newMessageTree.message))
            self.graphNodes = {0: self.root}
            # Associate the root graph node with message ID 0
            # for inverse-lookup purposes.
            self.graph.SetPyData(self.root, 0)
            self.reprintBranchSelectorText()
            for messageTree in newMessageTree.children:
                self.drawMessageTree(messageTree)
        else:
            for messageTree in newMessageTree.traverse():
                print (  "Drawing message from client " 
                       + str(messageTree.message.clientID) + ": "
                       + str(messageTree.message))
                if not "\n" in str(messageTree.message):
                    self.graphNodes[messageTree.message.ID] = \
                        self.graph.AppendItem(
                            self.graphNodes[messageTree.message.parentID], 
                            (  self.nicks[messageTree.message.clientID] + "<"
                             + self.twoCharStrings[messageTree.message.ID]
                             + ">  " + str(messageTree.message))
                            )
                else:
                    self.graphNodes[messageTree.message.ID] = \
                        self.graph.AppendItem(
                            self.graphNodes[messageTree.message.parentID], 
                            (  self.nicks[messageTree.message.clientID] + "<"
                             + self.twoCharStrings[messageTree.message.ID]
                             + ">\n" + str(messageTree.message))
                            )
                    print "Setting fixed font on " + str(messageTree.message)
                    self.graph.SetItemFont(
                        self.graphNodes[messageTree.message.ID],
                        self.fixed
                        )
                # Associate the graph node with its message ID
                # for inverse-lookup purposes.
                self.graph.SetPyData(
                    self.graphNodes[messageTree.message.ID],
                    messageTree.message.ID
                    )
            self.graph.ExpandAll()
            self.graph.ScrollTo(self.graphNodes[newMessageTree.message.ID])

    def assignTwoCharStrings(self, newMessageTree):
        for messageTree in newMessageTree.traverse():
            self.twoCharTuple = self.twoCharTuples.next()
            self.twoCharStrings[messageTree.message.ID] = \
                self.twoCharTuple[0] + self.twoCharTuple[1]

    def listen(self, client):
        # Expect first message tree to be the base message tree.
        newMessageTree = client.messageTreeOut.get()
        self.assignTwoCharStrings(newMessageTree)
        self.drawMessageTree(newMessageTree, True)
        while True:
            # Wait until the client processes a message, then redraw the graph.
            newMessageTree = client.messageTreeOut.get()
            self.assignTwoCharStrings(newMessageTree)
            self.drawMessageTree(newMessageTree)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
