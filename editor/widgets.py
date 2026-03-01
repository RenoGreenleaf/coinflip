# Copyright (C) 2026  Reno Greenleaf
import typing
from qtpy.QtWidgets import QTreeWidgetItem
from qtpy.QtCore import Qt
from editor import protocols


class Branch(QTreeWidgetItem):
	def __init__(self, piece: protocols.Node):
		super().__init__([str(piece)])
		self.piece = piece

	def build(self):
		self.setFlags(
			self.flags()
			| Qt.ItemFlag.ItemIsEditable
			| Qt.ItemFlag.ItemIsDragEnabled
			| Qt.ItemFlag.ItemIsDropEnabled
		)

		if len(self.piece.children) == 0:
			return

		for node in self.piece.children:
			item = Branch(node)
			self.addChild(item)
			item.build()

	def setData(self, column: int, role: int, value: str):
		self.piece.describe(value)
		return super().setData(column, role, str(self.piece))
