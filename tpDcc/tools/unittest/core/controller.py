#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget controller class implementation
"""

from __future__ import print_function, division, absolute_import


class UnitTestController(object):
    def __init__(self, client, model):

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model
