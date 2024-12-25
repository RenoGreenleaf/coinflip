class Editor:
	def __init__(self, cli, events, scenes):
		self.cli = cli
		self.events = events
		self.scenes = scenes
		self.current_editable = self

	def edit(self):
		command = input(f'{self.current_editable}> ')

		if command == 'exit':
			exit()
		elif command == 'back':
			self.current_editable = self
		else:
			self.current_editable.editable_execute(command)

	def editable_execute(self, command):
		if command == 'list':
			self._list()
		elif command.startswith('select '):
			_, scene_name = command.split(' ')
			scene = self.scenes[scene_name]
			self.current_editable = scene
		else:
			self.cli.print("Unclear.")

	def _list(self):
		self.cli.print("Events:")

		for event_name in self.events:
			self.cli.print("\t", event_name)

		self.cli.print("Scenes:")

		for scene_name in self.scenes:
			self.cli.print("\t", scene_name)

	def __repr__(self):
		return 'all'
