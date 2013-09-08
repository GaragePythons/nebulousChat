import wx

class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='nebulousChat')

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        dummyAddress = "123.456.789.123:9999"

        self.tree = wx.TreeCtrl(
            self.panel, wx.ID_ANY, wx.DefaultPosition, 
            (-1,-1), wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|
            wx.TR_NO_LINES)
        self.root = self.tree.AddRoot("<" + dummyAddress + "> First ever nebC conversation!")
        self.firstReply = self.tree.AppendItem(self.root, "<GP> This is the first ever reply.\nIt contains a newline.")
        self.secondReply = self.tree.AppendItem(self.firstReply, "<AB> nebulousChat is shit. This reply is a particularly long one, with many characters.")
        self.thirdReply = self.tree.AppendItem(self.root, "<CD> Another reply to the subject.")
        self.fourthReply = self.tree.AppendItem(self.firstReply, "<GP> Obligatory reply acknowledging that nebC is shit.")

        self.tree.ExpandAll()

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=wx.ID_ANY)

        nickStr = "GP"
        self.nickButton = wx.Button(self.panel, wx.ID_ANY, "<" + nickStr + ">")

        self.prompt = wx.TextCtrl(
            self.panel, style=wx.TE_PROCESS_ENTER)
        self.prompt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        topSizer.Add(self.tree, 1, wx.EXPAND, 5)

        bottomSizer.Add(self.nickButton, 0, wx.CENTRE)
        bottomSizer.Add(self.prompt, 1, wx.CENTRE)

        mainSizer.Add(topSizer, 1, wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(bottomSizer, 0, wx.EXPAND, 5)

        self.panel.SetSizer(mainSizer)
        topSizer.Fit(self)
        self.SetSize(wx.Size(800,600))

    def OnSelChanged(self, event):
        item = event.GetItem()

    def OnEnter(self, event):
        msg = self.prompt.GetValue()
        self.prompt.Clear()
        self.tree.AppendItem(self.root, "<GP> " + msg)


# Run the program
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
