from cmd2 import Cmd


class Player(Cmd):
	prompt = "> "
	def __init__(self, location, pool):
		super().__init__()
		self.model = location
		self.pool = pool  # pool is needed because it provides a session

	def interact(self):
		self.cmdloop()

	def do_look(self, args):
		if args != 'around':
			print("Unclear.")
			return

		with self.pool.get_db_session() as session:
			session.add(self.model)
			print(self.model.description)

	def complete_look(self, text, line, begidx, endidx):
		return ['around']
