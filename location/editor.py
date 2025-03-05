from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = "location> "

	def event_choices(self):
		events = self.pool.get_all_events()
		return [CompletionItem(event.id, str(event)) for event in events]

	def exit_choices(self):
		return [CompletionItem(exit_.id, exit_.name) for exit_ in self.model.exits]

	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument(
		'event_id',
		choices_provider=event_choices,
		type=int
	)

	exits_parser = Cmd2ArgumentParser()
	exits_parser.add_argument('exit_id', choices_provider=exit_choices, type=int)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		new_description = input("New description for the location:\n")

		if new_description:
			self.model.description = new_description
			self._update_model()

		self.cmdloop()
		state['current'] = None

	@with_argparser(events_parser)
	def do_discovered(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.set_discovered_event(int(args.event_id))
			session.commit()

	def do_list(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			print(self.model.description)
			print(f"Discovered event: {self.model.discovered_event}")

			for exit_ in self.model.exits:
				print(f"\t{exit_.id} {exit_} (triggers {exit_.triggers_event})")

	def do_exit(self, args):
		print("Going back.")
		return True

	@with_argparser(exits_parser)
	def do_delete(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.delete_exit(args.exit_id)
			session.commit()
			print(f"Exit #{args.exit_id} is removed.")

	@with_argparser(events_parser)
	def do_add(self, args):
		name = input("Name of the exit:\n") or "nameless"

		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.add_exit(name=name, triggers_event_id=args.event_id)
			session.commit()

	@with_argparser(exits_parser)
	def do_rename(self, args):
		new_name = input("New name: ")

		with self.pool.get_db_session() as session:
			exit_ = self.model.find_exit_by_id(args.exit_id)
			session.add(exit_)
			exit_.name = new_name
			session.commit()

	@with_argparser(exits_parser)
	def do_describe(self, args):
		description = input("New description:\n")

		with self.pool.get_db_session() as session:
			session.add(self.model)
			exit_ = self.model.find_exit_by_id(args.exit_id)
			exit_.description = description
			session.commit()

	def _update_model(self):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			session.commit()
