from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser


class Editor(Cmd):
	"""Common editor functionality to reduce code duplication."""
	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		self.cmdloop()
		state['path'].pop()

	def do_exit(self, args):
		print("Leaving the editor.")
		return True

	def do_list(self, args):
		print(self.model)


def event_choices(editor):
	events = editor.pool.get_all_events()
	return [CompletionItem(event.id, str(event)) for event in events]


events_parser = Cmd2ArgumentParser()
events_parser.add_argument(
	'event_id',
	choices_provider=event_choices,
	type=int
)


def is_event_id(identifier, pool):
	ids = set(event.id for event in pool.get_all_events())

	if identifier not in ids:
		print(f"There's no event with ID {identifier}.")
		return False
	else:
		return True
