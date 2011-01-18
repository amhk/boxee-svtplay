class DownloadQueue:
	def __init__(self):
		# FIXME: should be initialized from database
		self.queue = [
			"6c759d63139ed317c39c67cf4d9bc319ae6b6d1f",
			"846b2e4f0df06d53da9e851156426fc0ce6bcb75"
		]

	def asList(self):
		return self.queue
