import wx
from api import m
from . import player
class Window(wx.Frame):
	def __init__(self, parent=None):
		super().__init__(parent, title="pubPlayer")
		panel=wx.Panel(self)
		boxlabel=wx.StaticText(panel, label="&Publication list: ")
		self.list_box=wx.ListBox(panel, choices=m.texts)
		self.list_box.SetSelection(0)
		btn_play=wx.Button(panel, label="&Play")
		btn_play.Bind(wx.EVT_BUTTON, self.onPlay)
		btn_close=wx.Button(panel, label="&Exit")
		btn_close.Bind(wx.EVT_BUTTON, self.onClose)
		self.list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.onPlay)
		self.Bind(wx.EVT_CLOSE, self.onClose)

		self.Show()
		wx.CallAfter(self.list_box.SetFocus)

	def onPlay(self, event):
		text=self.list_box.GetStringSelection()
		if not text:
			return
		index=m.texts.index(text)
		entry=m.items[index]
		kind=entry[0]
		element=entry[1]
		if kind=="stream":
			urls=m.stream_urls(element)
		else:
			urls=m.audio_urls(element)
		try:
			stream=player.create_stream(urls)
			player.Window(stream, element["title"], self)
		except Exception as e:
			wx.MessageBox(f"Could not play: {e}", "Error", wx.ICON_ERROR)

	def onClose(self, event):
		self.Destroy()
