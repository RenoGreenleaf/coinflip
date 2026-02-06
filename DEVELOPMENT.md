# Board-Player-Handler

The approach is based on MVC pattern.

There's a board containing in-game objects (pieces). It's generally passive. The only thing it should actively do is trigger events. It (and its pieces) doesn't listen to events though. A board corresponds to a _model_ in MVC.

There're players. They listen to events and manipulate (observe and change) a board. The term player here is broader than in its traditional sense. It means not only people and AI players, but also various subsystems handling physics, navigation, directing etc. A player corresponds to a _view_ in MVC.

A player has access to a board, but when it does changes (writing, editing) to it, the recommended way to perform them is through a handler. Handler helps to decouple board and a player. A handler corresponds to a _controller_ in MVC.
