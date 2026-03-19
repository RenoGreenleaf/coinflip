# Copyright (C) 2026  Reno Greenleaf
"""Root widget."""
import json
from typing import cast
import qtpynodeeditor as ne
from qtpy import QtWidgets as widgets, QtGui as gui
from coinflip.protocols import Persistent
from editor import players
from terminal.pieces import Conversation, Option
from coinflip.board import World
from editor.widgets import Branch, Tree


class Window(widgets.QMainWindow):
	"""An app needs a main window."""

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.last_id = 0
		self.tree = Tree()
		super().__init__()

	def build(self):
		"""Prepare base layout. Call it right after instantiation."""
		self.tree.setHeaderLabels(['Piece'])
		self.tree.setDragEnabled(True)
		self.tree.setAcceptDrops(True)
		self.tree.setDropIndicatorShown(True)
		self.tree.setDragDropMode(
			widgets.QAbstractItemView.DragDropMode.InternalMove
		)
		world = World(identifier=1)
		root = Branch(world)
		root.build()
		self.tree.insertTopLevelItem(0, root)

		scroller = widgets.QScrollArea()
		scroller.setWidgetResizable(True)
		scroller.setWidget(self.tree)

		root = widgets.QWidget()
		root_layout = widgets.QHBoxLayout(root)

		registry = ne.DataModelRegistry()
		registry.register_model(players.Option)
		registry.register_model(players.Conjunction)
		scene = players.Scene(registry=registry)
		flow = ne.FlowView(scene)
		flow.setAcceptDrops(True)

		root_layout.addWidget(scroller)
		root_layout.addWidget(flow)
		self.setCentralWidget(root)

		toolbar = widgets.QToolBar()
		toolbar.setMovable(False)
		self.addToolBar(toolbar)

		add = gui.QAction("Add", self)
		add.triggered.connect(self.add)
		delete = gui.QAction("Delete", self)
		delete.triggered.connect(self.delete)
		save = gui.QAction("Save", self)
		save.triggered.connect(self.save)
		load = gui.QAction("Load", self)
		load.triggered.connect(self.load)
		toolbar.addAction(add)
		toolbar.addAction(delete)
		toolbar.addAction(save)
		toolbar.addAction(load)

	def add(self):
		"""Add piece. Called via UI."""
		selection = cast(Branch, self.tree.currentItem())
		zeroRoot = self.tree.invisibleRootItem()

		if zeroRoot is None:
			return

		if selection is None:
			selection = cast(Branch, zeroRoot.child(0))

		if selection.piece.type == 'option':
			current_conversation = selection.parent()
		elif selection.piece.type == 'conversation':
			current_conversation = selection
		elif selection.piece.type == 'world':
			self._insert_conversation()
			return
		else:
			raise Exception("Can't find a conversation to add an option to.")

		if current_conversation is None:
			raise Exception("There's no root piece.")

		option = Option(
			description='<no description>',
			identifier=self._generate_id()
		)
		current_conversation = cast(Branch, current_conversation)
		branch = Branch(option)
		branch.build()
		current_conversation.addChild(branch)

	def save(self):
		"""Preserve current state to a file."""
		path, _ = widgets.QFileDialog.getSaveFileName(self)

		if path == '':
			return

		with open(path, 'w', encoding='utf-8') as world_file:
			json.dump(self.normalize(), world_file, indent=4)

	def load(self):
		"""Restore state from a file."""
		relationships = {}
		path, _ = widgets.QFileDialog.getOpenFileName(self)

		if path == '':
			return

		with open(path, 'r', encoding='utf-8') as world_file:
			self.denormalize(json.load(world_file), relationships)

	def normalize(self) -> dict:
		"""Prepare raw data for saving."""
		zeroRoot = self.tree.invisibleRootItem()

		if zeroRoot is None:
			raise Exception("There's no board.")

		root = zeroRoot.child(0)

		if root is None:
			raise Exception("There's no world.")

		world = cast(Branch, root).piece

		view = self.findChild((ne.FlowView,))
		return {
			'ai': cast(players.Scene, view.scene).normalize(),
			'board': cast(Persistent, world).model_dump(),
		}

	def denormalize(self, raw_world: dict, relationships: dict) -> None:
		"""Fill a window from raw data."""
		self.tree.clear()
		raw_board = raw_world['board']
		board = World(**raw_board)
		root = Branch(board)
		root.build()
		root.persist(relationships)
		self.tree.insertTopLevelItem(0, root)

		view = self.findChild((ne.FlowView,))
		cast(players.Scene, view.scene).denormalize(raw_world, relationships)

	def delete(self):
		root = self.tree.invisibleRootItem()
		for branch in self.tree.selectedItems():
			parent = branch.parent() or root

			if parent is None:
				continue

			parent.removeChild(branch)

	def _generate_id(self) -> int:
		iterator = widgets.QTreeWidgetItemIterator(self.tree)
		current = 0

		while iterator.value():
			current = max(current, cast(Branch, iterator.value()).piece.identifier)
			iterator += 1

		return current + 1

	def _insert_conversation(self):
		# get world
		zeroRoot = self.tree.invisibleRootItem()

		if zeroRoot is None:
			return

		root = zeroRoot.child(0)

		if root is None:
			return

		# add conversation
		piece = Conversation(
			subject='<nameless>',
			identifier=self._generate_id()
		)
		branch = Branch(piece)
		branch.build()

		root.addChild(branch)
