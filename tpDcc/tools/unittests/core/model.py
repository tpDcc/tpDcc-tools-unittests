#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget model class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Signal, QObject


class UnitTestModel(QObject, object):

    treeModelChanged = Signal(object)

    def __init__(self):
        super(UnitTestModel, self).__init__()

        self._tree_model = None

    @property
    def tree_model(self):
        return self._tree_model

    @tree_model.setter
    def tree_model(self, value):
        self._tree_model = value
        self.treeModelChanged.emit(self._tree_model)
