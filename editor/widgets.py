# Copyright (C) 2026  Reno Greenleaf
from typing import cast
from qtpy import QtGui
from qtpy.QtWidgets import QAbstractItemView, QTreeWidget, QTreeWidgetItem
from qtpy.QtCore import Qt, Signal
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
			super().addChild(item)
			item.build()

	def setData(self, column: int, role: int, value: str):
		self.piece.describe(value)
		return super().setData(column, role, str(self.piece))

	def persist(self, relationships: dict):
		relationships[str(self.piece.identifier)] = self

		for offset in range(self.childCount()):
			branch = cast(Branch, self.child(offset))
			branch.persist(relationships)

	def addChild(self, child: QTreeWidgetItem|None):
		if child is None:
			return

		branch = cast(Branch, child)
		self.piece.children.append(branch.piece)
		return super().addChild(branch)

	def removeChild(self, child: QTreeWidgetItem|None):
		if child is None:
			return

		branch = cast(Branch, child)
		self.piece.children.remove(branch.piece)
		branch.cascade_notification()
		return super().removeChild(child)

	def cascade_notification(self):
		tree = cast(Tree, self.treeWidget())
		tree.removing.emit(self)

		for offset in range(self.childCount()):
			branch = cast(Branch, self.child(offset))
			tree.removing.emit(branch)
			branch.cascade_notification()

	def depth(self):
		count = 1
		parent = self.parent()

		while parent is not None:
			parent = parent.parent()
			count += 1

		return count


class Tree(QTreeWidget):
	removing = Signal(Branch)

	def dropEvent(self, event: QtGui.QDropEvent | None):
		is_near = (
			QAbstractItemView.DropIndicatorPosition.AboveItem,
			QAbstractItemView.DropIndicatorPosition.BelowItem
		)

		if event is None:
			return

		items = self.selectedItems()

		if items == []:
			return super().dropEvent(event)

		item = cast(Branch, items[0])
		model_index = self.indexAt(event.position().toPoint())
		position = self.dropIndicatorPosition()

		if not model_index.isValid():
			return  # no drops to root or empty space

		target_item = self.itemFromIndex(model_index)

		if target_item is None:
			return

		if position in (QAbstractItemView.DropIndicatorPosition.OnItem,):
			intended_parent = target_item
		elif position in is_near:
			intended_parent = target_item.parent()
		else:
			return

		if intended_parent is None:
			return

		if cast(Branch, intended_parent).depth() + 1 != item.depth():
			return

		old_parent = cast(Branch, item.parent())
		super().dropEvent(event)
		new_parent = cast(Branch,item.parent())
		new_index = self.indexFromItem(item).row()

		index = old_parent.piece.children.index(item.piece)
		piece = old_parent.piece.children.pop(index)
		new_parent.piece.children.insert(new_index, piece)
