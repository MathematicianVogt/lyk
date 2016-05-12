import pafy
class audiofile:
	def __init__(self,url):
		self.video=pafy.new(url)
	def get_audio(self):
		best_audio = self.video.getbestaudio()
		x=best_audio.download()
		print x



v=audiofile("https://www.youtube.com/watch?v=6bEdzi_1dYs")
v.get_audio()

