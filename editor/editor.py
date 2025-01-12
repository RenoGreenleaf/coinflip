import cmd


class Editor(cmd.Cmd):
	prompt = '> '

	def __init__(self, cli, events, scenes):
		super().__init__()
		self.cli = cli
		self.events = events
		self.scenes = scenes
		self._set_current_editable(self)

	def do_list(self, args):
		"""Overview of instances for editing."""
		if self.current_editable is not self:
			print('\n'.join(self.current_editable.list()))
			return

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
		self._set_current_editable(self)

	def do_select(self, args):
		"""Make further commands to be applied to selected instance."""
		scene_name = args.split(' ')[0]
		scene = self.scenes.get(scene_name)

		if scene:
			self._set_current_editable(scene)
		else:
			self.cli.print(f"There's no scene \"{scene_name}\".")

	def complete_list(self, text, line, begidx, endidx):
		return [c for c in ('scenes', 'events') if c.startswith(text)]

	def complete_select(self, text, line, begidx, endidx):
		return [name for name in self.scenes if name.startswith(text)]

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

	def _set_current_editable(self, editable):
		"""Prevents code duplication."""
		self.current_editable = editable
		self.prompt = f"{editable}> "

	def __repr__(self):
		return 'all'
