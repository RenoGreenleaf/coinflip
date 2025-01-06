import cmd


class Editor(cmd.Cmd):
	prompt = '> '

	def __init__(self, cli, events, scenes):
		super().__init__()
		self.cli = cli
		self.events = events
		self.scenes = scenes
		self.current_editable = self

	def do_list(self, args):
		"""Overview of instances for editing."""
		group = args.split(' ')[0]

		if group == '' or group == 'events':
			self._list_events()

		if group == '' or group == 'scenes':
			self._list_scenes()

	def do_exit(self, args):
		"""Leave entirely."""
		self.cli.exit()

	def do_back(self, args):
		"""Leave currently selected instance."""

	def do_select(self, args):
		"""Make further commands to be applied to selected instance."""
		scene_name = args.split(' ')[0]
		scene = self.scenes.get(scene_name)

		if scene:
			self.current_editable = scene
			self.prompt = f"{scene}> "
		else:
			self.cli.print(f"There's no scene \"{scene_name}\".")

	def complete_list(self, text, line, begidx, endidx):
		return [c for c in ('scenes', 'events') if c.startswith(text)]

	def complete_select(self, text, line, begidx, endidx):
		return [name for name in self.scenes if name.startswith(text)]

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

	def emptyline(self):
		"""Default emptyline() behaviour isn't acceptable."""

	def _list_events(self):
		self.cli.print("Events:")

		for event_name in self.events:
			self.cli.print("\t", event_name)

	def _list_scenes(self):
		self.cli.print("Scenes:")

		for scene_name in self.scenes:
			self.cli.print("\t", scene_name)

	def __repr__(self):
		return 'all'
