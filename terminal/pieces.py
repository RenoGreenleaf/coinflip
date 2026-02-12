# Copyright (C) 2026  Reno Greenleaf
from coinflip.protocols import Player
from coinflip.pieces import Piece


class Option(Piece):
	description: str = ""
	message: str = ""
	permanent: bool = False
	hidden: bool = True

	def __init__(self):
		super().__init__()

		self.description = ""
		self.message = ""
		self.permanent = False
		self.hidden = True


	def load(self, raw: dict, relationships: dict):
		self.description = raw['description']
		self.message = raw['message']
		self.permanent = raw['permanent']
		self.hidden = raw['hidden']

	def save(self):
		return {
			'description': self.description,
			'message': self.message,
			'permanent': self.permanent,
			'hidden': self.hidden,
		}
