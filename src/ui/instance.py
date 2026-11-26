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
			total_pages=m.connect(instance)
		except Exception as e:
			wx.MessageBox(str(e), "Error", wx.ICON_ERROR)
			self.Destroy()
			return
		pages_dialog=PagesDialog(self, total_pages)
		if pages_dialog.ShowModal()!=wx.ID_OK:
			pages_dialog.Destroy()
			return
		pages=pages_dialog.GetValue()
		pages_dialog.Destroy()
		try:
			busy=wx.BusyInfo(f"Loading {pages} page(s) of audios, please wait...")
			try:
				m.load_audios(pages)
			finally:
				del busy
			main_window.Window()
			self.Destroy()
		except Exception as e:
			wx.MessageBox(str(e), "Error", wx.ICON_ERROR)
			self.Destroy()


	def onCancel(self, event):
		self.Destroy()

class PagesDialog(wx.Dialog):
	def __init__(self, parent, total_pages):
		super().__init__(parent, title="Pages to load")
		self.total_pages=total_pages
		panel=wx.Panel(self)
		info=wx.StaticText(panel, label=f"This instance has {total_pages} page(s) of audios, with 30 audios per page.")
		warning=wx.StaticText(panel, label="Warning: the more pages you load, the longer the audios will take to load.")
		label=wx.StaticText(panel, label="&Number of pages to load:")
		self.spin=wx.SpinCtrl(panel, min=1, max=total_pages, initial=1)
		btn_ok=wx.Button(panel, id=wx.ID_OK, label="&OK")
		btn_ok.SetDefault()
		btn_cancel=wx.Button(panel, id=wx.ID_CANCEL, label="&Cancel")
		self.spin.SetFocus()

	def GetValue(self):
		return self.spin.GetValue()