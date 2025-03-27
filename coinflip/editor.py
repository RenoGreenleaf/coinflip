from cmd2 import Cmd2ArgumentParser, with_argparser
from reusables import editor


class Editor(editor.Editor):
	prompt = "coin flip> "
	threshold_parser = Cmd2ArgumentParser()
	threshold_parser.add_argument('threshold', type=int)

	@with_argparser(editor.events_parser)
	def do_won(self, args):
		if not editor.is_event_id(args.event_id, self.pool):
			return

		self.model.won_event = self.pool.get_event(args.event_id)

	@with_argparser(threshold_parser)
	def do_threshold(self, args):
		self.model.set_threshold(args.threshold)
		print(f"Victory threshold is now {self.model.victory_threshold}.")
