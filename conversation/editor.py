from cmd2 import Cmd2ArgumentParser, with_argparser, CompletionItem
from reusables import editor


class Editor(editor.Editor):
	prompt = "conversation> "

	def option_choices(self):
		"""Selection of an option for updating."""
		index = 0

		for option in self.model.options:
			yield CompletionItem(index, str(option))
			index += 1

	options_parser = Cmd2ArgumentParser()
	options_parser.add_argument(
		'index',
		choices_provider=option_choices,
		type=int
	)

	def interact(self, state):
		self.state = state
		self.cmdloop()

	def do_add(self, args):
		option = self.model.add_option()
		self.state['path'].append(option)
		return True

	@with_argparser(options_parser)
	def do_update(self, args):
		option = self.model.get_option(args.index)
		self.state['path'].append(option)
		return True

	@with_argparser(options_parser)
	def do_delete(self, args):
		print("Removing the option.")
		self.model.delete_option(args.index)

	def do_list(self, args):
		print(self.model)

		for option in self.model.options:
			print(f"\t{option}")

	def do_exit(self, args):
		print("Leaving conversation editor.")
		self.state['path'].pop()
		return True


class OptionEditor(editor.Editor):
	prompt = ("option> ")

	def boolean_choice(self):
		return ['true', 'false']

	boolean_parser = Cmd2ArgumentParser()
	boolean_parser.add_argument(
		'choice',
		choices_provider=boolean_choice
	)

	def do_list(self, state):
		print(f"Description: {self.model.description}")
		print(f"Triggers: {self.model.triggers}")
		print(f"Hidden by: {self.model.hide}")
		print(f"Shown by: {self.model.show}")
		print(f"Is available by default: {self.model.available}")
		print(f"Message: {self.model.message}")

	def do_description(self, args):
		print("Updating description.")
		self.model.description = args

	@with_argparser(editor.events_parser)
	def do_triggers(self, args):
		if not editor.is_event_id(args.event_id, self.pool):
			return

		print("Setting triggering event.")
		self.model.triggers = self.pool.get_event(args.event_id)

	@with_argparser(editor.events_parser)
	def do_hide(self, args):
		if not editor.is_event_id(args.event_id, self.pool):
			return

		print("Setting hiding event.")
		self.model.hide = self.pool.get_event(args.event_id)

	@with_argparser(editor.events_parser)
	def do_show(self, args):
		if not editor.is_event_id(args.event_id, self.pool):
			return

		print("Setting showing event.")
		self.model.show = self.pool.get_event(args.event_id)

	@with_argparser(boolean_parser)
	def do_available(self, args):
		print("Setting availability.")
		choice = True if args.choice == 'true' else False
		self.model.available = choice

	def do_message(self, args):
		print("Updating message.")
		self.model.message = args
