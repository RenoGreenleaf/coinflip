class Lock:
	def __init__(self):
		self.position = 0

	def prepare(self):
		self.pins = [True, True, False, True]

	def turn(self, is_clockwise):
		if self.pins[self.position] == is_clockwise:
			self.position += 1
			return True
		else:
			self.position = 0
			return False

	def unlocked(self):
		return self.position == len(self.pins)