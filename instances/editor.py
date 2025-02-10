from cmd import Cmd
from reusables.session import Session


class Editor(Cmd):
	def __init__(self, events):
		super().__init__()
		self.events = events

	def interact(self):
		self.cmdloop()

	def do_list(self, args):
		for identifier, event in self.events.items():
			print(f"{identifier} {event}")

	def do_delete(self, args):
		event = self.events.pop(int(args))

		with Session() as session:
			session.delete(event)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		return True

	# TODO: following functions require state machine

	def do_create(self, args):
		pass

	def do_update(self, args):
		pass
