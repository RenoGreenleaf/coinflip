from cmd2 import Cmd
from reusables.session import Session


class Editor(Cmd):
	prompt = "room> "

	def __init__(self, room):
		super().__init__()
		self.model = room

	def interact(self, state):
		new_description = input("New description for the room:\n")

		if new_description:
			self.model.description = new_description
			self._update_model()

		self.cmdloop()
		state['current'] = None

	def do_list(self, args):
		print(self.model.description)

		for exit_ in self.model.exits:
			print(f"\t{exit_.id} {exit_}")

	def do_exit(self, args):
		print("Going back.")
		return True

	def do_delete(self, args):
		exit_ = self.model.find_exit_by_name(args)

		with Session() as session:
			self.model.exits.remove(exit_)
			session.add(self.model)
			session.commit()

		print(f"{exit_} is removed.")

	def do_add(self, args):
		name = input("Name of the exit:\n")

		if not name:
			return

		with Session() as session:
			self.model.add_exit(name=name)
			session.add(self.model)
			session.commit()

	def do_rename(self, args):
		new_name = input("New name: ")

		with Session() as session:
			exit_ = self.model.find_exit_by_name(args)
			exit_.name = new_name
			session.add(exit_)
			session.commit()

	def complete_delete(self, text, line, begidx, endidx):
		return self._exits_names_autocomplete(text)

	def complete_rename(self, text, line, begidx, endidx):
		return self._exits_names_autocomplete(text)

	def _exits_names_autocomplete(self, text):
		exits = self.model.find_exits(text)
		return [exit_.name for exit_ in exits]

	def _update_model(self):
		with Session() as session:
			session.add(self.model)
			session.commit()
