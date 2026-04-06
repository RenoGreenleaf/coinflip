# Copyright (C) 2026  Reno Greenleaf
"""Making sure widgets are ready to be mapped to JSON data."""
import tempfile
import os
from qtpy import QtWidgets as widgets
from qtpynodeeditor import FlowView
from coinflip.board import World
from coinflip.pieces import Piece
from editor.players import Option
from editor.widgets import Branch
from window import Window


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
	assert hasattr(model, 'scenee')
