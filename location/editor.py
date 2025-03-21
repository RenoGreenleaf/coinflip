from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = "location> "

	def event_choices(self):
		events = self.pool.get_all_events()
		return [CompletionItem(event.id, str(event)) for event in events]

	def exit_choices(self):
		index = 0

		for exit_ in self.model.exits:
			yield CompletionItem(index, str(exit_))
			index += 1

	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument(
		'event_id',
		choices_provider=event_choices,
		type=int
	)

	exits_parser = Cmd2ArgumentParser()
	exits_parser.add_argument('index', choices_provider=exit_choices, type=int)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		new_description = input("New description for the location:\n")

		if new_description:
			self.model.description = new_description

		self.cmdloop()
		state['path'].pop()

	@with_argparser(events_parser)
	def do_discovered(self, args):
		self.model.discovered_event = self.pool.get_event(args.event_id)

	def do_list(self, args):
		print(self.model.description)
		print(f"Discovered event: {self.model.discovered_event}")

		for exit_ in self.model.exits:
			print(f"\t{exit_} (triggers {exit_.triggers_event})")

	def do_exit(self, args):
		print("Going back.")
		return True

	@with_argparser(exits_parser)
	def do_delete(self, args):
		self.model.delete_exit(args.index)
		print(f"Exit #{args.index} is removed.")

	@with_argparser(events_parser)
	def do_add(self, args):
		name = input("Name of the exit:\n") or "nameless"
		self.model.add_exit(
			name=name,
			triggers_event=self.pool.get_event(args.event_id)
		)

	@with_argparser(exits_parser)
	def do_rename(self, args):
		new_name = input("New name: ")
		self.model.exits[args.index].name = new_name

	@with_argparser(exits_parser)
	def do_describe(self, args):
		description = input("New description:\n")
		self.model.exits[args.index].description = description
