from cmd import Cmd
from reusables.session import Session
from event.models import Event
from ending.models import Ending


class Editor(Cmd):
	def __init__(self, pool):
		super().__init__()
		self.pool = pool

	def interact(self, current_editable):
		self.current_editable = current_editable
		self.cmdloop()

	def do_list(self, args):
		print("Events:")

		for identifier, event in self.pool['events'].items():
			print(f"\t{identifier} {event}")

		print("Scenes:")

		for identifier, scene in self.pool['scenes'].items():
			print(f"\t{identifier} {scene}")

	def do_delete(self, args):
		event = self.pool['events'].pop(int(args))

		with Session() as session:
			session.delete(event)
			session.commit()

	def do_exit(self, args):
		print("Leaving.")
		exit()

	def do_create(self, args):
		new_event = Event(name="New Event")
		self.current_editable[0] = new_event
		return True

	def do_update(self, args):
		self.current_editable[0] = self.pool['events'][int(args)]
		return True
