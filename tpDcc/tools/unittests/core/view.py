#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget view class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt
from Qt.QtWidgets import QSizePolicy, QMenuBar, QToolBar, QAction, QSplitter, QAbstractItemView

from tpDcc import dcc
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import dividers, views

from tpDcc.tools.unittests.widgets import console


class UnitTestView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(UnitTestView, self).__init__(parent=parent)

        self._menu_bar = self._setup_menubar()
        self._tool_bar = self._setup_toolbar()

        splitter = QSplitter(Qt.Horizontal, parent=self)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._tree_view = views.BaseTreeView(parent=self)
        self._tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._console = console.Console(parent=self)
        splitter.addWidget(self._tree_view)
        splitter.addWidget(self._console)
        splitter.setStretchFactor(1, 4)

        self.main_layout.addWidget(self._menu_bar)
        self.main_layout.addWidget(self._tool_bar)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(splitter)

        self.refresh()

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def ui(self):
        super(UnitTestView, self).ui()

    def setup_signals(self):
        pass

    def refresh(self):
        pass

    def _setup_menubar(self):
        menubar = QMenuBar(parent=self)
        settings_menu = menubar.addMenu('Settings')
        help_menu = menubar.addMenu('Help')

        if dcc.is_maya():
            pass

        return menubar

    def _setup_toolbar(self):
        toolbar = QToolBar(parent=self)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        run_all_tests_action = QAction('Run All Tests', parent=self)

        for action in [run_all_tests_action]:
            toolbar.addAction(action)

        return toolbar
