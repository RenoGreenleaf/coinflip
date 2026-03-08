# Copyright (C) 2026  Reno Greenleaf
"""Root widget."""
import json
from typing import cast
from pydantic import BaseModel
import qtpynodeeditor as ne
from qtpy import QtWidgets as widgets, QtGui as gui
from editor import players
from editor.protocols import Node
from terminal.pieces import Conversation, Option
from coinflip.board import World
from editor.widgets import Branch


class Window(widgets.QMainWindow):
	"""An app needs a main window."""

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.last_id = 0
		self.tree = widgets.QTreeWidget()
		super().__init__()

	def build(self):
		"""Prepare base layout. Call it right after instantiation."""
		self.tree.setHeaderLabels(['Piece'])
		self.tree.setDragEnabled(True)
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
		"""Add option. Called via UI."""
		selection = cast(Branch, self.tree.currentItem())

		if selection is None:
			selection = self.tree.invisibleRootItem().child(0)

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

		with open(path, 'w', encoding='utf-8') as world_file:
			json.dump(self.normalize(), world_file, indent=4)

	def load(self):
		"""Restore state from a file."""
		relationships = {}
		path, _ = widgets.QFileDialog.getOpenFileName(self)
		options = self.findChildren((Option,))

		for option in options:
			option.deleteLater()

		with open(path, 'r', encoding='utf-8') as world_file:
			self.denormalize(json.load(world_file), relationships)

	def normalize(self) -> dict:
		"""Prepare raw data for saving."""
		world: BaseModel = self.tree.invisibleRootItem().child(0).piece

		view = self.findChild((ne.FlowView,))
		return {
			'ai': view.scene.normalize(),
			'board': world.model_dump(),
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
		view.scene.denormalize(raw_world, relationships)

	def delete(self):
		root = self.tree.invisibleRootItem()
		for branch in self.tree.selectedItems():
			parent = branch.parent() or root
			parent.removeChild(branch)

	def _generate_id(self):
		iterator = widgets.QTreeWidgetItemIterator(self.tree)
		current = 0

		while iterator.value():
			current = max(current, iterator.value().piece.identifier)
			iterator += 1

		return current + 1

	def _insert_conversation(self):
		piece: Node = Conversation(
			subject='<nameless>',
			identifier=self._generate_id()
		)
		branch = Branch(piece)
		branch.build()
		root = self.tree.invisibleRootItem().child(0)
		root.addChild(branch)
