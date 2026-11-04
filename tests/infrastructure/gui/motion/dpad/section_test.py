# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for MotionDpadSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.dpad.isection import IMotionDpadSection
from botracked.infrastructure.gui.motion.dpad.section import MotionDpadSection
from botracked.infrastructure.gui.motion.dpad.trigger.itrigger import IMotionTrigger
from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionDpadSectionTest(TestCase):
    '''
        Tests MotionDpadSection headless widget wiring and state changes.
    '''

    @patch('botracked.infrastructure.gui.motion.dpad.section.Button')
    @patch('botracked.infrastructure.gui.motion.dpad.section.Frame')
    def test_section_actions_and_state(
        self, mock_frame_cls: MagicMock, mock_btn_cls: MagicMock
    ) -> None:
        '''
            Verifies D-pad button grid creation, triggers, and enable toggle.

            :param mock_frame_cls: Patched Frame class.
            :param mock_btn_cls: Patched Button class.
            :exceptions: None.
        '''
        mock_btn = MagicMock()
        mock_btn_cls.return_value = mock_btn
        delegate = MagicMock(spec=IMotionActionDelegate)
        triggers = {
            cmd: MagicMock(spec=IMotionTrigger)
            for cmd in (
                MotionCommand.FORWARD,
                MotionCommand.BACKWARD,
                MotionCommand.TURN_LEFT,
                MotionCommand.TURN_RIGHT,
                MotionCommand.SPIN_LEFT,
                MotionCommand.SPIN_RIGHT,
            )
        }
        sec = MotionDpadSection(MagicMock(spec=Frame), delegate, triggers)
        self.assertIsInstance(sec, IMotionDpadSection)
        self.assertIs(sec.get_widget(), mock_frame_cls.return_value)
        sec.trigger_motion(MotionCommand.FORWARD)
        delegate.handle_motion.assert_called_once_with(MotionCommand.FORWARD)
        sec.trigger_stop()
        delegate.handle_stop.assert_called_once()
        sec.set_enabled(False)
        mock_btn.configure.assert_called_with(state='disabled')
        sec.set_enabled(True)
        mock_btn.configure.assert_called_with(state='normal')


if __name__ == '__main__':
    main()
