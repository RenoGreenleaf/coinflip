from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser


class Player(Cmd):
	prompt = "> "

	def look_around(self, args):
		print("Looking around.")
		print(self.model.description)

	def look_at(self, args):
		print(f"Looking at {args.exit}.")
		exit_ = self.model.find_exit_by_name(args.exit)
		print(exit_.description)

	def look_at_choices(self):
		return [exit_.name for exit_ in self.model.find_exits('')]

	# look at/around
	look_parser = Cmd2ArgumentParser()
	look_subparsers = look_parser.add_subparsers()
	at_parser = look_subparsers.add_parser('at')
	at_parser.add_argument('exit', choices_provider=look_at_choices)
	around_parser = look_subparsers.add_parser('around')
	at_parser.set_defaults(func=look_at)
	around_parser.set_defaults(func=look_around)

	def __init__(self, location, pool):
		super().__init__()
		self.model = location
		self.pool = pool  # pool is needed because it provides a session

	def interact(self):
		self.cmdloop()

	@with_argparser(look_parser)
	def do_look(self, args):
		function = getattr(args, 'func', None)

		if function:
			function(self, args)
		else:
			print("Unclear.")

	def do_leave(self, args):
		self.model.discovered_event.trigger()
		return True

	def do_use(self, args):
		name = args.strip('"')
		print(f"You're going through {name}.")
		exit_ = self.model.find_exit_by_name(name)
		exit_.triggers_event.trigger()
		return True

	def complete_use(self, text, line, begidx, endidx):
		return [exit_.name for exit_ in self.model.find_exits(text)]
