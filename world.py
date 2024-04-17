class World(dict):
	"""Container for objects shared among scenes."""
	def __init__(self):
		super().__init__()
		self['events'] = set()