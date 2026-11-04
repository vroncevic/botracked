# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Provides MotionKeyboardController handling WASD/Space hotkeys safely.
'''

from __future__ import annotations

from tkinter import Event, Tk, Widget
from tkinter.ttk import Frame
from typing import ClassVar

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionKeyboardController:
    '''
        Defines class MotionKeyboardController implementing
        IMotionKeyboardController without loose lambdas.
        Suppresses hotkeys when focus resides inside text input widgets.

        It defines:

            :attributes:
                | KEY_PRESS_SEQ - Tkinter key press event sequence.
                | IGNORED_WIDGETS - Widget classes where typing must not steer.
                | _delegate - Motion action delegate port.
                | _enabled - Boolean flag enabling hotkey dispatch.
            :methods:
                | __init__ - Initializes controller with motion delegate.
                | bind_to - Binds <KeyPress> event on target window.
                | on_key_press - Matches WASD/Space keys outside text inputs.
                | set_enabled - Enables or disables hotkey teleoperation.
                | is_enabled - Returns current enabled state.
    '''

    KEY_PRESS_SEQ: ClassVar[str] = '<KeyPress>'
    IGNORED_WIDGETS: ClassVar[tuple[str, ...]] = ('Text', 'Entry', 'TCombobox')

    _delegate: IMotionActionDelegate
    _enabled: bool

    def __init__(self, delegate: IMotionActionDelegate) -> None:
        '''
            Initializes keyboard controller with motion action delegate.

            :param delegate: Motion action delegate port.
            :exceptions: None.
        '''
        self._delegate = delegate
        self._enabled = True

    def bind_to(self, window: Frame | Tk) -> None:
        '''
            Binds <KeyPress> event on target window to on_key_press.

            :param window: Target frame or root window to bind.
            :exceptions: None.
        '''
        window.bind(self.KEY_PRESS_SEQ, self.on_key_press)

    def on_key_press(self, event: Event) -> None:
        '''
            Matches WASD and Space hotkeys while ignoring text editors.

            :param event: Tkinter KeyPress Event instance.
            :exceptions: None.
        '''
        if not self._enabled:
            return

        if (
            isinstance(event.widget, Widget)
            and event.widget.winfo_class() in self.IGNORED_WIDGETS
        ):
            return

        match event.keysym.lower():
            case 'w':
                self._delegate.handle_motion(MotionCommand.FORWARD)
            case 's':
                self._delegate.handle_motion(MotionCommand.BACKWARD)
            case 'a':
                self._delegate.handle_motion(MotionCommand.TURN_LEFT)
            case 'd':
                self._delegate.handle_motion(MotionCommand.TURN_RIGHT)
            case 'space':
                self._delegate.handle_stop()
            case _:
                pass

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables hotkey teleoperation.

            :param enabled: True if active, False otherwise.
            :exceptions: None.
        '''
        self._enabled = enabled

    def is_enabled(self) -> bool:
        '''
            Returns current enabled state.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._enabled
