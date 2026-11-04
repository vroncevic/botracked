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
    Unit tests for MotionPanel composite component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.motion.dependencies import MotionPanelDependencies
from botracked.infrastructure.gui.motion.dpad.isection import IMotionDpadSection
from botracked.infrastructure.gui.motion.ipanel import IMotionPanel
from botracked.infrastructure.gui.motion.keyboard.controller.icontroller import (
    IMotionKeyboardController,
)
from botracked.infrastructure.gui.motion.panel import MotionPanel
from botracked.infrastructure.gui.motion.speed.isection import IMotionSpeedSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionPanelTest(TestCase):
    '''
        Tests MotionPanel delegation to D-pad, speed, and keyboard sub-ports.
    '''

    @patch('botracked.infrastructure.gui.motion.panel.Label')
    def test_panel_delegation(self, _lbl_cls: MagicMock) -> None:
        '''
            Verifies speed accessors, enable state propagation, and key bind.

            :param _lbl_cls: Patched Label class.
            :exceptions: None.
        '''
        frame = MagicMock(spec=Frame)
        dpad = MagicMock(spec=IMotionDpadSection)
        speed = MagicMock(spec=IMotionSpeedSection)
        speed.get_speed.return_value = 175
        kb = MagicMock(spec=IMotionKeyboardController)
        deps = MotionPanelDependencies(
            frame=frame,
            dpad_section=dpad,
            speed_section=speed,
            keyboard_controller=kb,
        )
        panel = MotionPanel(deps)
        self.assertIsInstance(panel, IMotionPanel)
        self.assertIs(panel.get_widget(), frame)
        self.assertEqual(panel.get_speed(), 175)
        panel.set_speed(200)
        speed.set_speed.assert_called_once_with(200)
        panel.set_enabled(False)
        dpad.set_enabled.assert_called_once_with(False)
        speed.set_enabled.assert_called_once_with(False)
        kb.set_enabled.assert_called_once_with(False)
        win = MagicMock(spec=Frame)
        panel.bind_keyboard(win)
        kb.bind_to.assert_called_once_with(win)


if __name__ == '__main__':
    main()
