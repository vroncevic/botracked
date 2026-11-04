# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    botracked is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    botracked is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for LayoutBuilder.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.connection.ipanel import IConnectionPanel
from botracked.infrastructure.gui.console.ipanel import IConsolePanel
from botracked.infrastructure.gui.layout.builder import LayoutBuilder
from botracked.infrastructure.gui.layout.bundle import GuiPanelsBundle
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.infrastructure.gui.motion.ipanel import IMotionPanel
from botracked.infrastructure.gui.telemetry.ipanel import ITelemetryPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class LayoutBuilderTest(TestCase):
    '''
        Tests LayoutBuilder split-pane mounting of cockpit panels.
    '''

    @patch('botracked.infrastructure.gui.layout.builder.Frame')
    def test_mount_layout(self, mock_frame_cls: MagicMock) -> None:
        '''
            Verifies create_slots and mount_layout pack all five panels cleanly.

            :param mock_frame_cls: Patched ttk Frame constructor.
            :exceptions: None.
        '''
        root = MagicMock(spec=Tk)
        builder = LayoutBuilder(root=root)
        slots = builder.create_slots()
        panels = GuiPanelsBundle(
            connection=MagicMock(spec=IConnectionPanel),
            mission=MagicMock(spec=IMissionPanel),
            motion=MagicMock(spec=IMotionPanel),
            telemetry=MagicMock(spec=ITelemetryPanel),
            console=MagicMock(spec=IConsolePanel),
        )
        central = builder.mount_layout(slots, panels)
        self.assertIs(central, slots.central_frame)
        self.assertTrue(mock_frame_cls.called)
        self.assertIs(builder.get_root(), root)


if __name__ == '__main__':
    main()
