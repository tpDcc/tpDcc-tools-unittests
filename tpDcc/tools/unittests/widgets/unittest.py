#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that contains unit test tree nodes models
"""

from __future__ import print_function, division, absolute_import


class BaseUnitTestTreeNodeModel(object):

    def __init__(self, parent=None):
        self.children = []
        self._parent = parent

        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        """
        Add a child to the node
        :param int child: Child node to add
        """

        if child not in self.children:
            self.children.append(child)

    def remove(self):
        """
        Remove this node and all its children from the tree
        """

        if self._parent:
            row = self.getRow()
            self._parent.children.pop(row)
            self._parent = None
        for child in self.children:
            child.remove()

    def child(self, row):
        """
        Get the child at the specified index
        :param int row: The child index
        :return: The tree node at the given index or None if the index was out of bounds
        """

        try:
            return self.children[row]
        except IndexError:
            return None

    def childCount(self):
        """
        Get the number of children in the node
        """

        return len(self.children)

    def parent(self):
        """
        Get the parent of node
        """

        return self._parent

    def row(self):
        """
        Get the index of the node relative to the parent
        """

        if self._parent is not None:
            return self._parent.children.index(self)
        return 0

    def data(self, column):
        """
        Get the table display data
        """

        return ''
