from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser
from reusables import editor


class Editor(editor.Editor):
	prompt = "location> "

	def exit_choices(self):
		index = 0

		for exit_ in self.model.exits:
			yield CompletionItem(index, str(exit_))
			index += 1

	exits_parser = Cmd2ArgumentParser()
	exits_parser.add_argument('index', choices_provider=exit_choices, type=int)

	def interact(self, state):
		new_description = input("New description for the location:\n")

		if new_description:
			self.model.description = new_description

		self.cmdloop()
		state['path'].pop()

	@with_argparser(editor.events_parser)
	def do_discovered(self, args):
		self.model.discovered_event = self.pool.get_event(args.event_id)

	def do_list(self, args):
		print(self.model.description)
		print(f"Discovered event: {self.model.discovered_event}")

		for exit_ in self.model.exits:
			print(f"\t{exit_} (triggers {exit_.triggers_event})")

	@with_argparser(exits_parser)
	def do_delete(self, args):
		self.model.delete_exit(args.index)
		print(f"Exit #{args.index} is removed.")

	@with_argparser(editor.events_parser)
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
