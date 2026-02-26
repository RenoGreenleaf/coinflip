# Copyright (C) 2026  Reno Greenleaf
from qtpy.QtWidgets import QTreeWidgetItem
from editor import protocols


class TreeItem(QTreeWidgetItem):
	def __init__(self, piece: protocols.Node):
		super().__init__([str(piece)])
		self.piece = piece

	def branch(self):
		if len(self.piece.children) == 0:
			return

		for node in self.piece.children:
			item = TreeItem(node)
			self.addChild(item)
			item.branch()
