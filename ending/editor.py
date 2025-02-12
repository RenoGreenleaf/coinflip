from reusables.session import Session


class Editor():
	def __init__(self, model):
		super().__init__()
		self.model = model

	def interact(self, current_editable):
		new_message = input("New message to be shown when ending:\n")

		if not new_message:
			current_editable[0] = None
			return

		self.model.message = new_message

		with Session() as session:
			session.add(self.model)
			session.commit()

		current_editable[0] = None
