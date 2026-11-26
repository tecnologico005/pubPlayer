import json
import urllib.request
LISTEN_URL_STREAMS="https://live.audiopub.site"
class Pub():
	def __init__(self):
		self.instance=None
		self.audio_list=[]
		self.stream_list=[]
		self.items=[]
		self.texts=[]

	def normalize(self, instance):
		instance=instance.strip().rstrip("/")
		if instance=="":
			raise Exception("No instance was entered.")
		if not instance.startswith(("http://", "https://")):
			instance="https://"+instance
		return instance

	def get_json(self, path):
		request=urllib.request.Request(f"{self.instance}{path}", headers={"Accept": "application/json", "User-Agent": "pubPlayer"})
		try:
			with urllib.request.urlopen(request, timeout=15) as response:
				return json.loads(response.read().decode("utf-8"))
		except Exception as e:
			raise Exception(f"Could not connect to the instance: {e}") from e

	def format_user(self, item):
		user=item.get("user")
		if user is None:
			return "unknown"
		name=user.get("name")
		if not name:
			return "unknown"
		display_name=user.get("displayName")
		if not display_name:
			display_name=name
		return f"{display_name} (@{name})"

	def format_audio(self, audio):
		user=self.format_user(audio)
		description=audio.get("description") or ""
		description=" ".join(description.split())
		if not description:
			description="No description"
		return f"{user}: {audio['title']}: {description}"

	def format_stream(self, stream):
		user=self.format_user(stream)
		description=stream.get("description") or ""
		description=" ".join(description.split())
		if not description:
			description="No description"
		return f"[LIVE NOW] {user}: {stream['title']}: {description}"

	def decode(self, flat):
		cache={}
		def read(i):
			if i==-1:
				return None
			if i in cache:
				return cache[i]
			value=flat[i]
			if isinstance(value, dict):
				result={}
				cache[i]=result
				for key, ref in value.items():
					result[key]=read(ref)
				return result
			if isinstance(value, list):
				result=[]
				cache[i]=result
				for ref in value:
					result.append(read(ref))
				return result
			return value
		return read(0)

	def extract_front_page(self, data):
		for node in data.get("nodes", []):
			if node.get("type")!="data":
				continue
			root=self.decode(node["data"])
			if isinstance(root, dict) and "audios" in root:
				return root
		raise Exception("The instance did not return the audio list.")

	def load_audios(self, instance):
		self.instance=self.normalize(instance)
		front_page=self.extract_front_page(self.get_json("/__data.json"))
		self.audio_list=front_page.get("audios") or []
		self.stream_list=front_page.get("streams") or []
		self.items=[("stream", stream) for stream in self.stream_list]+[("audio", audio) for audio in self.audio_list]
		self.texts=[self.format_stream(stream) for stream in self.stream_list]+[self.format_audio(audio) for audio in self.audio_list]

	def audio_urls(self, audio):
		paths=[audio.get("url"), audio.get("transcodedUrl") or audio.get("transcodedPath")]
		return [f"{self.instance}/{path.lstrip('/')}" for path in paths if path]

	def stream_urls(self, stream):
		user_id=(stream.get("user") or {}).get("id")
		if not user_id:
			return []
		return [f"{LISTEN_URL_STREAMS}/{user_id}"]

m=Pub()
