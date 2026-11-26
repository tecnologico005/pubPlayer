import wx
from ui import instance
app=wx.App()
app.SetAppName("pubPlayer")
instance.Window()
app.MainLoop()