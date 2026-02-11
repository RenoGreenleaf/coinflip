# Copyright (C) 2026  Reno Greenleaf
"""Entry point."""
from qtpy.QtWidgets import QApplication
from editor.window import Window
from sys import argv


app = QApplication(argv)

window = Window()
window.build()
window.show()

app.exec()
