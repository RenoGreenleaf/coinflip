from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser


class Editor(Cmd):
	prompt = 'SM> '

	def scene_choices(self):
		scenes = self.pool.get_all_scenes()
		return [CompletionItem(scene.id, str(scene)) for scene in scenes]

	def event_choices(self):
		events = self.pool.get_all_events()
		return [CompletionItem(event.id, str(event)) for event in events]

	transitions_parser = Cmd2ArgumentParser()
	transitions_parser.add_argument('scene_id', choices_provider=scene_choices)
	transitions_parser.add_argument('event_id', choices_provider=event_choices)

	def __init__(self, model, pool):
		super().__init__()
		self.model = model
		self.pool = pool

	def interact(self, state):
		self.cmdloop()
		state['current'] = None

	def do_exit(self, args):
		return True

	def do_describe(self, args):
		with self.pool.get_db_session() as session:
			session.add(self.model)
			print(self.model)

			for transition in self.model.transitions:
				print(f"\t{transition.id} {transition}")

	@with_argparser(transitions_parser)
	def do_add(self, args):
		with self.pool.get_db_session() as session:
			scene_id = int(args.scene_id)
			event_id = int(args.event_id)
			self.model.add_transition(scene_id, event_id)
			session.add(self.model)
			session.commit()
