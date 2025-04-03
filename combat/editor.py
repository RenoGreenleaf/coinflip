from cmd2 import Cmd2ArgumentParser, with_argparser
from reusables import editor


class Editor(editor.Editor):
	prompt = "combat> "
	moves_parser = Cmd2ArgumentParser()
	moves_parser.add_argument('moves', nargs='+')

	@with_argparser(moves_parser)
	def do_ai_moves(self, args):
		self.model.ai_moves = args.moves
