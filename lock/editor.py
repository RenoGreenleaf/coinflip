from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, CompletionItem


class Editor(Cmd):
	prompt = "lock> "

	def get_directions(self):
		return ['clockwise', 'counterclockwise']

	def pins_choice(self):
		index = 0

		for pin in self.model.pins:
			yield CompletionItem(index, str(pin))
			index += 1

	def events_choice(self):
		return [
			CompletionItem(event.id, str(event))
			for event
			in self.pool.get_all_events()
		]

	directions_parser = Cmd2ArgumentParser()
	directions_parser.add_argument('direction', choices_provider=get_directions)
	pins_parser = Cmd2ArgumentParser()
	pins_parser.add_argument('index', choices_provider=pins_choice, type=int)
	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument('event_id', choices_provider=events_choice, type=int)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		self.cmdloop()
		state['path'].pop()

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

	@with_argparser(events_parser)
	def do_unlocked(self, args):
		self.model.unlocked_event = self.pool.get_event(args.event_id)

	def do_list(self, args):
		print(self.model)
		print(f"Unlocking triggers {self.model.unlocked_event}.")

		index = 0

		for pin in self.model.pins:
			print(f"\t#{index} {pin}")
			index += 1

	def do_exit(self, args):
		print("Leaving lock editor.")
		return True
