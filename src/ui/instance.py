import wx
from api import m
from . import main_window
class Window(wx.Dialog):
	def __init__(self, parent=None):
		super().__init__(parent, title="Audiopub instance")
		panel=wx.Panel(self)
		boxlabel=wx.StaticText(panel, label="Type the address of the audiopub instance here")
		self.box=wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.box.Bind(wx.EVT_TEXT_ENTER, self.onOk)
		btn_ok=wx.Button(panel, label="&OK")
		btn_ok.Bind(wx.EVT_BUTTON, self.onOk)
		btn_cancel=wx.Button(panel, label="&Cancel")
		btn_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
		self.Bind(wx.EVT_CLOSE, self.onCancel)
		self.box.SetFocus()
		self.Show()

	def onOk(self, event):
		instance=self.box.GetValue()
		try:
			m.load_audios(instance)
			main_window.Window()
			self.Destroy()
		except Exception as e:
			wx.MessageBox(str(e), "Error", wx.ICON_ERROR)
			self.Destroy()
			return


	def onCancel(self, event):
		self.Destroy()