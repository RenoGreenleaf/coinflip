from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = "location> "

	def event_choices(self):
		events = self.pool.get_all_events()
		return [CompletionItem(event.id, str(event)) for event in events]

	events_parser = Cmd2ArgumentParser()
	events_parser.add_argument('event_id', choices_provider=event_choices)

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

	def do_delete(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			exit_ = self.model.find_exit_by_name(args)
			self.model.exits.remove(exit_)
			session.commit()
			print(f"{exit_} is removed.")

	@with_argparser(events_parser)
	def do_add(self, args):
		name = input("Name of the exit:\n") or "nameless"

		with self.pool.get_db_session() as session:
			session.add(self.model)
			self.model.add_exit(name=name, triggers_event_id=args.event_id)
			session.commit()

	def do_rename(self, args):
		new_name = input("New name: ")

		with self.pool.get_db_session() as session:
			exit_ = self.model.find_exit_by_name(args)
			session.add(exit_)
			exit_.name = new_name
			session.commit()

	def do_describe(self, args):
		description = input("Description:\n")

		if not description:
			return

		with self.pool.get_db_session() as session:
			exit_ = self.model.find_exit_by_name(args)
			session.add(exit_)
			exit_.description = description
			session.commit()

	def complete_delete(self, text, line, begidx, endidx):
		return self._exits_names_autocomplete(text)

	def complete_rename(self, text, line, begidx, endidx):
		return self._exits_names_autocomplete(text)

	def complete_describe(self, text, line, begidx, endidx):
		return self._exits_names_autocomplete(text)

	def _exits_names_autocomplete(self, text):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			exits = self.model.find_exits(text)
			return [exit_.name for exit_ in exits]

	def _update_model(self):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			session.commit()
