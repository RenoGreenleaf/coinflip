from reusables.models import Scene


class Combat(Scene):
	def __init__(self):
		self.id = 0
		self.ai_moves = []
		self.rounds = []

	def save(self):
		result = {'rounds': [], 'ai_moves': []}
		result['id'] = self.id

		for move in self.ai_moves:
			result['ai_moves'].append(move.save())

		for round_ in self.rounds:
			result['rounds'].append(round_.save())

		return result

	def load(self, dictionary, pool):
		self.id = dictionary['id']

		for move_data in dictionary['ai_moves']:
			strategy = Strategy()
			strategy.load(move_data, pool)
			self.ai_moves.append(strategy)

		for round_data in dictionary['rounds']:
			round_ = Round()
			round.load(round_data, pool)
			self.rounds.append(round_)

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
