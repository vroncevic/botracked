# -*- coding: UTF-8 -*-

'''
Module
    ipanel.py
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
    Defines IMotionPanel protocol for composite manual motion panel.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Frame
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IMotionPanel(Protocol):
    '''
        Defines structural contract IMotionPanel for manual steering panel.

        It defines:

            :methods:
                | get_widget - Returns root container Frame widget.
                | get_speed - Returns current PWM speed integer value.
                | set_speed - Updates locomotion PWM speed setting.
                | set_enabled - Enables or disables motion controls and hotkeys.
                | bind_keyboard - Binds WASD and Space hotkeys to window.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Section Frame widget.
        '''

    def get_speed(self) -> int:
        '''
            Returns current PWM speed integer value.

            :return: Current speed integer.
        '''

    def set_speed(self, speed: int) -> None:
        '''
            Updates locomotion PWM speed setting.

            :param speed: New PWM speed integer.
        '''

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables motion controls and hotkeys.

            :param enabled: True if interactive, False otherwise.
        '''

    def bind_keyboard(self, window: Frame | Tk) -> None:
        '''
            Binds WASD and Space hotkeys to target window.

            :param window: Target frame or root window to bind.
        '''
