# Copyright (C) 2026  Reno Greenleaf
from qtpy.QtWidgets import QTreeWidgetItem
from qtpy.QtWidgets import QAbstractItemView
from editor import protocols


class Branch(QTreeWidgetItem):
	def __init__(self, piece: protocols.Node):
		super().__init__([str(piece)])
		self.piece = piece

	def build(self):
		if len(self.piece.children) == 0:
			return

		for node in self.piece.children:
			item = Branch(node)
			self.addChild(item)
			item.build()
