from reusables.models import Scene
from combat.editor import Editor, RoundEditor


class Combat(Scene):
	def __init__(self):
		self.id = 0
		self.ai_moves = []
		self.rounds = []

	def save(self):
		result = {'rounds': [], 'type': 'combat'}
		result['id'] = self.id
		result['ai_moves'] = self.ai_moves

		for round_ in self.rounds:
			result['rounds'].append(round_.save())

		return result

	def load(self, dictionary, pool):
		self.id = dictionary['id']
		self.ai_moves = dictionary['ai_moves']

		for round_data in dictionary['rounds']:
			round_ = Round()
			round_.load(round_data, pool)
			self.rounds.append(round_)

	def wrap_for_editing(self, pool):
		return Editor(self, pool)

	def add_round(self):
		round_ = Round()
		self.rounds.append(round_)
		return round_

	def __repr__(self):
		return f"Combat #{self.id}"


class Round:
	def __init__(self):
		self.outcomes = []

	def save(self):
		result = {'outcomes': []}

		for outcome in self.outcomes:
			result['outcomes'].append(outcome.save())

		return result

	def load(self, dictionary, pool):
		for outcome_data in dictionary['outcomes']:
			outcome = Outcome()
			outcome.load(outcome_data, pool)
			self.outcomes.append(outcome)

	def wrap_for_editing(self, pool):
		return RoundEditor(self, pool)

	def add_outcome(self, ai_strategy, players_strategy, next_round):
		outcome = Outcome()
		outcome.ai_strategy = ai_strategy
		outcome.players_strategy = players_strategy
		outcome.next_round = next_round
		self.outcomes.append(outcome)
		return outcome

	def __repr__(self):
		return f"Round with {len(self.outcomes)} Outcomes"


class Outcome:
	def __init__(self):
		self.ai_strategy = None
		self.players_strategy = None
		self.next_round = False

	def save(self):
		return {
			'ai_strategy': self.ai_strategy,
			'players_strategy': self.players_strategy,
			'next_round': self.next_round
		}

	def load(self, dictionary, pool):
		# currently strategies are represented as simple strings
		self.ai_strategy = dictionary['ai_strategy']
		self.players_strategy = dictionary['players_strategy']
		self.next_round = dictionary['next_round']

	def __repr__(self):
		return f"Outcome (AI: {self.ai_strategy}, P: {self.players_strategy})"
