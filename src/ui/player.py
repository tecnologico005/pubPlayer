import wx
from api import m
from sound_lib.output import Output
from sound_lib.stream import URLStream
output=None
def create_stream(urls):
	global output
	if output is None:
		output=Output()
	last_error=None
	for url in urls:
		try:
			return URLStream(url=url)
		except Exception as e:
			last_error=e
	raise Exception(str(last_error))
class Window(wx.Dialog):
	def __init__(self, stream, title, parent=None):
		super().__init__(parent, title=f"Playing: {title}")
		self.stream=stream
		self.muted=False
		self.volume=1.0
		panel=wx.Panel(self)
		btn_close=wx.Button(panel, label="&Close")
		btn_close.Bind(wx.EVT_BUTTON, self.onClose)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKey)
		self.stream.play()
		self.ShowModal()

	def onKey(self, event):
		key=event.GetKeyCode()
		if key==wx.WXK_F2:
			self.togglePlay()
		elif key==wx.WXK_F1:
			self.seek(-10)
		elif key==wx.WXK_F3:
			self.seek(10)
		elif key==wx.WXK_F4:
			self.toggleMute()
		elif key==wx.WXK_ESCAPE:
			self.onClose(event=None)
		else:
			event.Skip()

	def togglePlay(self):
		try:
			if self.stream.is_playing:
				self.stream.pause()
			else:
				self.stream.play()
		except Exception:
			pass

	def seek(self, seconds):
		try:
			position=self.stream.get_position()
			current=self.stream.bytes_to_seconds(position)
			target=max(0.0, current+seconds)
			target_bytes=self.stream.seconds_to_bytes(target)
			length=self.stream.get_length()
			if length>0:
				target_bytes=min(target_bytes, length)
			self.stream.set_position(target_bytes)
		except Exception:
			pass

	def toggleMute(self):
		try:
			if self.muted:
				self.stream.set_volume(self.volume)
				self.muted=False
			else:
				self.volume=self.stream.get_volume()
				self.stream.set_volume(0.0)
				self.muted=True
		except Exception:
			pass

	def onClose(self, event):
		self.stream.stop()
		self.stream.free()
		self.Destroy()
