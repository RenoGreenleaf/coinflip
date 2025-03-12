from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser, CompletionItem


class Editor(Cmd):
	prompt = "lock> "

	def get_directions(self):
		return ['clockwise', 'counterclockwise']

	def get_pins(self):
		return [CompletionItem(pin.offset, str(pin)) for pin in self.model.pins]

	def get_events(self):
		return [
			CompletionItem(event.id, str(event))
			for event
			in self.pool.get_all_events()
		]

	directions_parser = Cmd2ArgumentParser()
	directions_parser.add_argument('direction', choices_provider=get_directions)
	pins_parser = Cmd2ArgumentParser()
	pins_parser.add_argument('pin_offset', choices_provider=get_pins, type=int)
	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument('event_id', choices_provider=get_events, type=int)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		self.cmdloop()
		state['current'] = None

	@with_argparser(directions_parser)
	def do_create(self, args):
		is_clockwise = True if args.direction == 'clockwise' else False

		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.add_pin(is_clockwise)
			session.commit()

	@with_argparser(pins_parser)
	def do_delete(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.delete_pin(args.pin_offset)
			session.commit()

	@with_argparser(pins_parser)
	def do_switch(self, args):
		print(f"Switching pin {args.pin_offset}.")

		with self.pool.get_db_session() as session:
			session.add(self.model)
			is_clockwise = self.model.switch_pin(args.pin_offset)
			session.commit()

		direction = 'clockwise' if is_clockwise else 'counterclockwise'
		print(f"Pin #{args.pin_offset} is {direction} now.")

	@with_argparser(events_parser)
	def do_unlocked(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.set_unlocked(args.event_id)
			session.commit()

	def do_list(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			print(self.model)
			print(f"Unlocking triggers {self.model.unlocked_event}.")

			for pin in self.model.pins:
				print(f"\t{pin}")

	def do_exit(self, args):
		print("Leaving lock editor.")
		return True
