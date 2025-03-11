from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = "lock> "

	def get_directions(self):
		return ['clockwise', 'counterclockwise']

	directions_parser = Cmd2ArgumentParser()
	directions_parser.add_argument('direction', choices_provider=get_directions)

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

	def do_list(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			print(self.model)

			for pin in self.model.pins:
				print(f"\t{pin}")

	def do_exit(self, args):
		print("Leaving lock editor.")
		return True
