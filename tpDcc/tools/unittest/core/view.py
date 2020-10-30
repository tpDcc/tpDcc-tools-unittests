#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget view class implementation
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.qt.core import base


class UnitTestView(base.BaseWidget, object):
    def __init__(self, model, controller, parent=None):

        self._model = model
        self._controller = controller

        super(UnitTestView, self).__init__(parent=parent)

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
