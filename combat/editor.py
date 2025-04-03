from cmd2 import Cmd2ArgumentParser, with_argparser, CompletionItem
from reusables import editor


class Editor(editor.Editor):
	prompt = "combat> "

	def round_choices(self):
		index = 0

		for round_ in self.model.rounds:
			yield CompletionItem(index, str(round_))
			index += 1

	moves_parser = Cmd2ArgumentParser()
	moves_parser.add_argument('moves', nargs='+')

	round_parser = Cmd2ArgumentParser()
	round_parser.add_argument('index', choices_provider=round_choices, type=int)

	def interact(self, state):
		self.state = state
		self.cmdloop()

	@with_argparser(moves_parser)
	def do_ai_moves(self, args):
		self.model.ai_moves = args.moves

	def do_add_round(self, args):
		round_ = self.model.add_round()
		self.state['path'].append(round_)
		return True

	def do_list(self, args):
		print(self.model)
		print(f"AI moves: {", ".join(self.model.ai_moves)}")

	def do_exit(self, args):
		print("Leaving combat editor.")
		self.state['path'].pop()
		return True

	@with_argparser(round_parser)
	def do_update(self, args):
		if not args.index >= 0 or not args.index < len(self.model.rounds):
			print("The index is out of range.")
			return

		round_ = self.model.rounds[args.index]
		self.state['path'].append(round_)
		return True

	@with_argparser(round_parser)
	def do_delete(self, args):
		if not args.index >= 0 or not args.index < len(self.model.rounds):
			print("The index is out of range.")
			return

		del self.model.rounds[args.index]
		print("The round is removed.")


class RoundEditor(editor.Editor):
	prompt = "round> "

	def outcome_choices(self):
		index = 0

		for outcome in self.model.outcomes:
			yield CompletionItem(index, str(outcome))
			index += 1

	outcome_parser = Cmd2ArgumentParser()
	outcome_parser.add_argument('ai_strategy')
	outcome_parser.add_argument('players_strategy')
	outcome_parser.add_argument('next_round', choices=('true', 'false'))

	delete_parser = Cmd2ArgumentParser()
	delete_parser.add_argument(
		'index',
		type=int,
		choices_provider=outcome_choices
	)

	def do_list(self, args):
		print(self.model)
		print("\tAI\tPlayer")

		for outcome in self.model.outcomes:
			print(f"\t{outcome.ai_strategy}\t{outcome.players_strategy}")

	@with_argparser(outcome_parser)
	def do_add(self, args):
		self.model.add_outcome(
			args.ai_strategy,
			args.players_strategy,
			True if args.next_round == 'true' else False
		)
		print("The outcome is added.")

	@with_argparser(delete_parser)
	def do_delete(self, args):
		if not args.index >= 0 or not args.index < len(self.model.outcomes):
			print("The index is out of range.")
			return

		del self.model.outcomes[args.index]
		print("The outcome is removed.")
