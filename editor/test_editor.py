# Copyright (C) 2026  Reno Greenleaf
"""Making sure widgets are ready to be mapped to JSON data."""
import tempfile
import os
from qtpy import QtWidgets as widgets
from qtpy.QtCore import Qt
from qtpynodeeditor import FlowView
from coinflip.board import World
from coinflip.pieces import Piece
from editor.players import Option
from editor.widgets import Branch
from window import Window
from pytestqt.qtbot import QtBot


def test_ids(qtbot):
	window = Window()
	window.build()
	expected_id = 5

	window.add()
	window.add()
	window.add()
	id_ = window._generate_id()

	assert id_ == expected_id


def test_saving(qtbot, monkeypatch, tmp_path):
	path = tmp_path / 'empty.json'

	def mock_save_dialog(*args, **kwargs):
		return (path, 'JSON files (*.json)')

	monkeypatch.setattr(
		widgets.QFileDialog,
		'getSaveFileName',
		mock_save_dialog
	)
	window = Window()
	window.build()

	window.save()

	assert os.path.isfile(path)


def test_normalization_has_board(qtbot):
	window = Window()
	window.build()
	expected_result = {
		'identifier': 1,
		'type': 'world',
		'conversations': []
	}

	result = window.normalize()

	assert 'board' in result
	assert expected_result == result['board']


def test_denormalization(qtbot):
	normalized_conversation = {
		'identifier': 24,
        'type': 'conversation',
        'subject': "Entrance"
	}
	normalized_structure = {
		'ai': {
			'connections': [],
			'nodes': {}
		},
		'board': {
			'identifier': 1,
			'type': 'world',
			'conversations': [normalized_conversation]
		}
	}
	window = Window()
	window.build()

	window.denormalize(normalized_structure, {})
	conversation = window.tree.invisibleRootItem().child(0).child(0).piece

	assert conversation.identifier == 24
	assert str(conversation) == "Entrance"


def test_no_child(qtbot):
	branch = Branch(World())

	result = branch.addChild(None)

	assert result is None


def test_option_initialized(qtbot):
	window = Window()
	window.build()
	view = window.findChild((FlowView,))
	scene = view.scene

	node = scene.create_node(Option)
	model = node.model

	assert hasattr(model, 'widget')
	assert hasattr(model, 'node')
	assert hasattr(model, 'scene')


def test_add_conversation(qtbot):
	window = Window()
	window.build()

	window.add()
	root = window.tree.invisibleRootItem()

	conversation = root.child(0).child(0)
	assert conversation.piece.type == 'conversation'


def test_add_option(qtbot):
	window = Window()
	window.build()
	window._insert_conversation()
	selection = window.tree.invisibleRootItem().child(0).child(0)
	window.tree.setCurrentItem(selection)

	window.add()
	added = window.tree.invisibleRootItem().child(0).child(0).child(0)

	assert added.piece.type == 'option'


def test_rename_conversation(qtbot: QtBot, qapp):
	window = Window()
	window.build()
	window.show()
	window._insert_conversation()
	window.tree.expandAll()
	conversation = window.tree.invisibleRootItem().child(0).child(0)
	rectangle = window.tree.visualItemRect(conversation)
	text = "New conversation"

	qtbot.mouseClick(window.tree.viewport(), Qt.LeftButton, pos=rectangle.center())
	qtbot.mouseDClick(window.tree.viewport(), Qt.LeftButton, pos=rectangle.center())
	qtbot.wait(10)
	widget = qapp.focusWidget()
	qtbot.keyClicks(widget, text)
	qtbot.wait(10)
	qtbot.keyClick(widget, Qt.Key_Enter)
	qtbot.wait(10)

	assert str(conversation.piece) == text
