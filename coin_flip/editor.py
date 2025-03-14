from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = "coin flip> "

	def event_choices(self):
		events = self.pool.get_all_events()
		return [CompletionItem(event.id, str(event)) for event in events]

	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument('event_id', choices_provider=event_choices)

	threshold_parser = Cmd2ArgumentParser()
	threshold_parser.add_argument('threshold', type=int)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		self.cmdloop()
		state['path'].pop()

	@with_argparser(events_parser)
	def do_won(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.set_won_event(int(args.event_id))
			session.commit()

	def do_exit(self, args):
		print("Leaving coin-flip editor.")
		return True

	@with_argparser(threshold_parser)
	def do_threshold(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.set_threshold(args.threshold)
			session.commit()
			print(f"Victory threshold is now {self.model.victory_threshold}.")
