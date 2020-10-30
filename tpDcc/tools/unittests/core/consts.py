#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains constant definitions for tpDcc-tools-unittest
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.python import python

if python.is_python2():
    from tpDcc.libs.python.enum import Enum
else:
    from enum import Enum


class UnitTestStatus(Enum):

    NOT_RUN = 0
    SUCCESS = 1
    FAIL = 2
    ERROR = 3
    SKIPPED = 4
