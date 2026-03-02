# Copyright (C) 2026  Reno Greenleaf
"""Root widget."""
import json
from typing import cast
import qtpynodeeditor as ne
from qtpy import QtWidgets as widgets, QtGui as gui
from editor import nodes
from terminal.pieces import Option
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
		self.setFixedHeight(600)
		self.setFixedWidth(800)

		self.tree.setHeaderLabels(['Piece'])
		self.tree.setDragEnabled(True)

		scroller = widgets.QScrollArea()
		scroller.setWidgetResizable(True)
		scroller.setWidget(self.tree)

		root = widgets.QWidget()
		root_layout = widgets.QHBoxLayout(root)

		registry = ne.DataModelRegistry()
		registry.register_model(nodes.Option)
		registry.register_model(nodes.Conjunction)
		scene = nodes.Scene(registry=registry)
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
		save = gui.QAction("Save", self)
		save.triggered.connect(self.save)
		load = gui.QAction("Load", self)
		load.triggered.connect(self.load)
		toolbar.addAction(add)
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
			current_conversation = selection.child(0)
		else:
			raise Exception("Can't find a conversation to add an option to.")

		if current_conversation is None:
			raise Exception("There's no root piece.")

		option = Option(
			description='<no description>',
			identifier=self._generate_id()
		)
		current_conversation = cast(Branch, current_conversation)
		current_conversation.piece.children.append(option)
		branch = Branch(option)
		current_conversation.addChild(branch)

	def save(self):
		"""Preserve current state to a file."""
		path, _ = widgets.QFileDialog.getSaveFileName(self)

		with open(path, 'w', encoding='utf-8') as world_file:
			json.dump(self.normalize(), world_file, indent=4)

	def load(self):
		"""Restore state from a file."""
		path, _ = widgets.QFileDialog.getOpenFileName(self)
		options = self.findChildren((Option,))

		for option in options:
			option.deleteLater()

		with open(path, 'r', encoding='utf-8') as world_file:
			self.denormalize(json.load(world_file))

	def normalize(self) -> dict:
		"""Prepare raw data for saving."""
		options = self.findChildren((Option,))
		normalized_options = {
			option.objectName(): option.normalize()
			for option in options
		}

		view = self.findChild((ne.FlowView,))
		return {
			'ai': view.scene.normalize(),
			'available': normalized_options,
		}

	def denormalize(self, raw_world: dict) -> None:
		"""Fill a window from raw data."""
		raw_board = raw_world['board']
		board = World(**raw_board)
		root = Branch(board)
		root.build()
		self.tree.insertTopLevelItem(0, root)

		# view = self.findChild((ne.FlowView,))
		# view.scene.denormalize(raw_world, self)

		# ids = map(int, raw_world['children'].keys())
		# self.last_id = max(ids)

	def _generate_id(self):
		iterator = widgets.QTreeWidgetItemIterator(self.tree)
		current = 0

		while iterator.value():
			current = max(current, iterator.value().piece.identifier)
			iterator += 1

		return current + 1
