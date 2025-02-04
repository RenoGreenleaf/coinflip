from tortoise import run_async
from cmd import Cmd


class Editor(Cmd):
	def __init__(self, model):
		super().__init__()
		self.model = model

	def do_list(self, args):
		print("Fields:")
		print(f"\tmessage: {self.model.message}")

	def do_exit(self, args):
		print("Leaving.")
		return True

	def do_edit(self, args):
		self.model.message = input("New message: ")
		run_async(self.model.save())
