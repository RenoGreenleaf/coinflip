from cmd import Cmd
from reusables.session import Session


class Editor(Cmd):
	def __init__(self, room):
		super().__init__()
		self.model = room

	def interact(self, current_editable):
		new_description = input("New description for the room:\n")

		if new_description:
			self.model.description = new_description
			self._update_model()

		self.cmdloop()
		current_editable[0] = None

	def do_list(self, args):
		print(self.model.description)

		for exit_ in self.model.exits:
			print(f"\t{exit_.id} {exit_}")

	def do_exit(self, args):
		print("Going back.")
		return True

	def _update_model(self):
		with Session() as session:
			session.add(self.model)
			session.commit()
