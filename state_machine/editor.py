from cmd2 import Cmd, CompletionItem, Cmd2ArgumentParser, with_argparser
from reusables import editor


class Editor(editor.Editor):
	prompt = 'SM> '

	def scene_choices(self):
		scenes = self.pool.get_all_scenes()
		return [CompletionItem(scene.id, str(scene)) for scene in scenes]

	def transitions_choices(self):
		index = 0

		for transition in self.model.transitions:
			yield CompletionItem(index, str(transition))
			index += 1

	transitions_parser = Cmd2ArgumentParser()
	transitions_parser.add_argument(
		'scene_id',
		choices_provider=scene_choices,
		type=int
	)
	transitions_parser.add_argument(
		'event_id',
		choices_provider=editor.event_choices,
		type=int
	)

	scenes_parser = Cmd2ArgumentParser()
	scenes_parser.add_argument(
		'scene_id',
		choices_provider=scene_choices,
		type=int
	)

	delete_parser = Cmd2ArgumentParser()
	delete_parser.add_argument(
		'index',
		choices_provider=transitions_choices,
		type=int
	)

	def do_list(self, args):
		print(self.model)
		print(f"Starts at {self.model.start}")

		index = 0

		for transition in self.model.transitions:
			print(f"\t{index} {transition}")
			index += 1

	@with_argparser(transitions_parser)
	def do_add(self, args):
		scene = self.pool.get_scene(args.scene_id)
		event = self.pool.get_event(args.event_id)
		self.model.add_transition(scene, event)

	@with_argparser(scenes_parser)
	def do_start(self, args):
		scene = self.pool.get_scene(args.scene_id)
		self.model.set_start(scene)

	@with_argparser(delete_parser)
	def do_delete(self, args):
		self.model.delete_transition(args.index)
		print("The transition is removed.")
