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

	def do_leave(self, args):
		self.model.discovered_event.trigger()
		return True

	def do_examine(self, args):
		exit_ = self.model.find_exit_by_name(args.strip('"'))
		print(exit_.description)

	def do_use(self, args):
		name = args.strip('"')
		print(f"You're going through {name}.")
		exit_ = self.model.find_exit_by_name(name)
		exit_.triggers_event.trigger()
		return True

	def complete_use(self, text, line, begidx, endidx):
		return [exit_.name for exit_ in self.model.find_exits(text)]

	def complete_examine(self, text, line, begidx, endidx):
		return [exit_.name for exit_ in self.model.find_exits(text)]

	def complete_look(self, text, line, begidx, endidx):
		return ['around']
