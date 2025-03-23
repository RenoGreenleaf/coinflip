from cmd2 import Cmd2ArgumentParser, with_argparser, CompletionItem
from reusables import editor


class Editor(editor.Editor):
	prompt = "lock> "

	def get_directions(self):
		return ['clockwise', 'counterclockwise']

	def pins_choice(self):
		index = 0

		for pin in self.model.pins:
			yield CompletionItem(index, str(pin))
			index += 1

	directions_parser = Cmd2ArgumentParser()
	directions_parser.add_argument('direction', choices_provider=get_directions)
	pins_parser = Cmd2ArgumentParser()
	pins_parser.add_argument('index', choices_provider=pins_choice, type=int)

	@with_argparser(directions_parser)
	def do_create(self, args):
		is_clockwise = True if args.direction == 'clockwise' else False
		self.model.add_pin(is_clockwise)

	@with_argparser(pins_parser)
	def do_delete(self, args):
		self.model.delete_pin(args.index)

	@with_argparser(pins_parser)
	def do_switch(self, args):
		print(f"Switching pin {args.index}.")
		is_clockwise = self.model.switch_pin(args.index)
		direction = 'clockwise' if is_clockwise else 'counterclockwise'
		print(f"Pin #{args.index} is {direction} now.")

	@with_argparser(editor.events_parser)
	def do_unlocked(self, args):
		self.model.unlocked_event = self.pool.get_event(args.event_id)

	def do_list(self, args):
		print(self.model)
		print(f"Unlocking triggers {self.model.unlocked_event}.")

		index = 0

		for pin in self.model.pins:
			print(f"\t#{index} {pin}")
			index += 1
