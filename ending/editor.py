from reusables.session import Session


class Editor():
	def __init__(self, model):
		super().__init__()
		self.model = model

	def interact(self, state):
		new_message = input("New message to be shown when ending:\n")
		state['current'] = None

		if not new_message:
			return

		self.model.message = new_message

		with Session() as session:
			session.add(self.model)
			session.commit()
