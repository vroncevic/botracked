# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for MissionPanel composite studio component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.mission.dependencies import MissionPanelDependencies
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.infrastructure.gui.mission.panel import MissionPanel
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection
from botracked.infrastructure.gui.mission.toolbar.isection import IMissionToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPanelTest(TestCase):
    '''
        Tests MissionPanel section mounting and delegation.
    '''

    @patch('botracked.infrastructure.gui.mission.panel.Label')
    def test_panel_methods(self, _lbl_cls: MagicMock) -> None:
        '''
            Verifies script and status delegation on MissionPanel.

            :param _lbl_cls: Patched Label class.
            :exceptions: None.
        '''
        frame = MagicMock(spec=Frame)
        status = MagicMock(spec=IMissionStatusSection)
        status.get_status_text.return_value = 'Ready'
        editor = MagicMock(spec=IMissionEditorSection)
        editor.get_script.return_value = 'STOP'
        toolbar = MagicMock(spec=IMissionToolbarSection)

        deps = MissionPanelDependencies(
            frame=frame,
            status_section=status,
            editor_section=editor,
            toolbar_section=toolbar,
            initial_script='STOP',
        )
        panel = MissionPanel(deps)
        self.assertIsInstance(panel, IMissionPanel)
        self.assertIs(panel.get_widget(), frame)
        editor.set_script.assert_called_once_with('STOP')
        self.assertEqual(panel.get_script(), 'STOP')
        panel.set_script('FORWARD 200')
        editor.set_script.assert_called_with('FORWARD 200')
        panel.set_status('Running', '#00FF88')
        status.set_status.assert_called_once_with('Running', '#00FF88')
        self.assertEqual(panel.get_status_text(), 'Ready')


if __name__ == '__main__':
    main()
