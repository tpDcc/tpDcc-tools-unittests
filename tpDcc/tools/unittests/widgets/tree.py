#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that contains unit test tree models
"""

from __future__ import print_function, division, absolute_import

import unittest

from Qt.QtCore import Qt, QModelIndex, QAbstractItemModel

from tpDcc.managers import resources
from tpDcc.libs.qt.core import qtutils

from tpDcc.tools.unittest.core import consts


class BaseUnitTestTreeModel(QAbstractItemModel, object):
    """
    The model used to populate the test tree view
    """

    def __init__(self, root, parent=None):
        super(BaseUnitTestTreeModel, self).__init__(parent)

        self.root_node = root

    def rowCount(self, parent):
        """
        Return the number of rows with this parent
        """

        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()
        return parent_node.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.name()
        elif role == Qt.DecorationRole:
            return node.get_icon()
        elif role == Qt.ToolTipRole:
            return node.toolTip

    def setData(self, index, value, role=Qt.EditRole):
        node = index.internalPointer()
        if qtutils.is_pyqt4() or qtutils.is_pyside():
            data_changed_kwargs = [index, index]
        else:
            data_changed_kwargs = [index, index, []]

        if role == Qt.EditRole:
            self.dataChanged.emit(*data_changed_kwargs)
            node.status = value
        if role == Qt.DecorationRole:
            node.status = value
            self.dataChanged.emit(*data_changed_kwargs)
            if node.parent() is not self.root_node:
                self.setData(self.parent(index), value, role)
        elif role == Qt.ToolTipRole:
            node.toolTip = value
            self.dataChanged.emit(*data_changed_kwargs)

    def headerData(self, section, orientation, role):
        return 'TreeModel'

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):
        node = index.internalPointer()
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()

        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def get_index_of_node(self, node):
        if node is self.root_node:
            return QModelIndex()
        return self.index(node.row(), 0, self.get_index_of_node(node.parent()))


class UnitTestTreeNodeModel(BaseUnitTestTreeModel, object):

    """
    A node representing a Test, TestCase or TestSuite for display in a QTreeView
    """

    def __init__(self, test, parent=None):
        super(UnitTestTreeNodeModel, self).__init__(parent=parent)
        self.test = test
        self.tool_tip = str(test)
        self.status = consts.UnitTestStatus.NOT_RUN

        if isinstance(self.test, unittest.TestSuite):
            for test_ in self.test:
                if isinstance(test_, unittest.TestCase) or test_.countTestCases():
                    self.add_child(UnitTestTreeNodeModel(test_, self))

    @staticmethod
    def success_icon():
        return resources.icon(name='ok')

    @staticmethod
    def fail_icon():
        return resources.icon(name='cancel')

    @staticmethod
    def error_icon():
        return resources.icon(name='high_priority')

    @staticmethod
    def skip_icon():
        return resources.icon(name='warning')

    def base_icon(self):
        return resources.icon(name='python')
        # if (isinstance(self.test, lib.MayaTestCase) or 'Maya' in self.name()):
        #     return resourcemanager.ResourceManager.icon(name='maya', theme='color', extension='png')
        # else:
        #     return resourcemanager.ResourceManager.icon(name='python', theme='color', extension='png')

    def name(self):

        """
        Get the name to print in the view
        """

        if isinstance(self.test, unittest.TestCase):
            return self.test._testMethodName
        elif isinstance(self.child(0).test, unittest.TestCase):
            return self.child(0).test.__class__.__name__
        else:
            return self.child(0).child(0).test.__class__.__module__

    def path(self):
        """
        Gets the import path of the test. Used for finding the test by name
        """

        if self.parent() and self.parent().parent():
            return '{0}.{1}'.format(self.parent().path(), self.name())
        else:
            return self.name()

    def get_status(self):
        """
        Get the status of the tpTestNode
        Nodes with children like the TestSuites, will get their status based on the
        status of the leaf nodes (the TestCases)
        @return: A status value from TestStatus
        """

        if not self.children:
            return self.status
        result = consts.UnitTestStatus.NOT_RUN
        for child in self.children:
            child_status = child.get_status()
            if child_status == consts.UnitTestStatus.ERROR:
                # Error status has highest priority so propagate that up to the parent
                return child_status
            elif child_status == consts.UnitTestStatus.FAIL:
                result = child_status
            elif child_status == consts.UnitTestStatus.SUCCESS and result != consts.UnitTestStatus.FAIL:
                result = child_status
            elif child_status == consts.UnitTestStatus.SKIPPED and result != consts.UnitTestStatus.FAIL:
                result = child_status
        return result

    def get_icon(self):
        """
        Get the status icon to display with the Test
        """

        status = self.get_status()
        return [self.base_icon(), self.success_icon(), self.fail_icon(), self.error_icon(), self.skip_icon()][status]
