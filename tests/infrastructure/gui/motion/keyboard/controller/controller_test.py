# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit tests for MotionKeyboardController.
'''

from __future__ import annotations

from tkinter import Event, Widget
from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate
from botracked.infrastructure.gui.motion.keyboard.controller.controller import (
    MotionKeyboardController,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionKeyboardControllerTest(TestCase):
    '''
        Tests MotionKeyboardController WASD/Space dispatch and text focus guard.
    '''

    def test_wasd_and_space_dispatch(self) -> None:
        '''
            Verifies w, s, a, d, space, and unknown keysym behavior.

            :exceptions: None.
        '''
        delegate = MagicMock(spec=IMotionActionDelegate)
        ctrl = MotionKeyboardController(delegate)
        win = MagicMock(spec=Frame)
        ctrl.bind_to(win)
        win.bind.assert_called_once_with('<KeyPress>', ctrl.on_key_press)

        for key_sym, expected in (
            ('w', MotionCommand.FORWARD),
            ('S', MotionCommand.BACKWARD),
            ('a', MotionCommand.TURN_LEFT),
            ('d', MotionCommand.TURN_RIGHT),
        ):
            ev: Event = Event()
            ev.keysym = key_sym
            ev.widget = None
            ctrl.on_key_press(ev)
            delegate.handle_motion.assert_called_with(expected)

        stop_ev: Event = Event()
        stop_ev.keysym = 'space'
        stop_ev.widget = None
        ctrl.on_key_press(stop_ev)
        delegate.handle_stop.assert_called_once()

        other_ev: Event = Event()
        other_ev.keysym = 'q'
        other_ev.widget = None
        ctrl.on_key_press(other_ev)

    def test_disabled_and_ignored_text_widget(self) -> None:
        '''
            Verifies hotkeys are suppressed when disabled or inside Text widget.

            :exceptions: None.
        '''
        delegate = MagicMock(spec=IMotionActionDelegate)
        ctrl = MotionKeyboardController(delegate)
        txt_widget = MagicMock(spec=Widget)
        txt_widget.winfo_class.return_value = 'Text'
        ev: Event = Event()
        ev.keysym = 'w'
        ev.widget = txt_widget
        ctrl.on_key_press(ev)
        delegate.handle_motion.assert_not_called()

        ctrl.set_enabled(False)
        self.assertFalse(ctrl.is_enabled())
        ev.widget = None
        ctrl.on_key_press(ev)
        delegate.handle_motion.assert_not_called()


if __name__ == '__main__':
    main()
