#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool taht allow to execute DCC specific unit tests
"""

from __future__ import print_function, division, absolute_import

import logging
import importlib

from tpDcc import dcc
from tpDcc.core import tool
from tpDcc.libs.qt.widgets import toolset
from tpDcc.tools.unittests.core import unittestclient

LOGGER = logging.getLogger('tpDcc-tools-unittests')

# Defines ID of the tool
TOOL_ID = 'tpDcc-tools-unittests'


class UnitTestsTool(tool.DccTool, object):
    def __init__(self, *args, **kwargs):
        super(UnitTestsTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Unit Tests',
            'id': TOOL_ID,
            'icon': 'unittest',
            'tooltip': 'Tool to execute unit tests inside DCCs.',
            'tags': ['tpDcc', 'dcc', 'tool', 'unit', 'test', 'unittest'],
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Unit Tests', 'load_on_startup': False, 'color': '', 'background_color': ''},
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


class UnitTestsToolsetWidget(toolset.ToolsetWidget, object):
    ID = TOOL_ID

    def __init__(self, *args, **kwargs):
        super(UnitTestsToolsetWidget, self).__init__(*args, **kwargs)

    def setup_client(self):

        self._client = unittestclient.UnitTestClient()
        self._client.signals.dccDisconnected.connect(self._on_dcc_disconnected)

        if not dcc.is_standalone():
            dcc_mod_name = '{}.dccs.{}.unittestserver'.format(TOOL_ID.replace('-', '.'), dcc.get_name())
            try:
                mod = importlib.import_module(dcc_mod_name)
                if hasattr(mod, 'UnitTestServer'):
                    server = mod.UnitTestServer(self, client=self._client, update_paths=False)
                    self._client.set_server(server)
                    self._update_client()
            except Exception as exc:
                LOGGER.warning(
                    'Impossible to launch Unit Test server! Error while importing: {} >> {}'.format(dcc_mod_name, exc))
                return
        else:
            self._update_client()

    def contents(self):

        from tpDcc.tools.unittests.core import model, view, controller

        unit_test_model = model.UnitTestModel()
        unit_test_controller = controller.UnitTestController(client=self._client, model=unit_test_model)
        unit_test_view = view.UnitTestView(model=unit_test_model, controller=unit_test_controller, parent=self)

        return [unit_test_view]
