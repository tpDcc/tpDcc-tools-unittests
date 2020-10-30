#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget model class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import QObject


class UnitTestModel(QObject, object):
    def __init__(self):
        super(UnitTestModel, self).__init__()
