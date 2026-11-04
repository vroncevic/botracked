# -*- coding: UTF-8 -*-

'''
Module
    isection.py
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
    Defines IMotionSpeedSection protocol for PWM speed slider leaf UI.
'''

from __future__ import annotations

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
class IMotionSpeedSection(Protocol):
    '''
        Defines structural contract IMotionSpeedSection for PWM speed slider.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | get_speed - Returns current PWM speed integer.
                | set_speed - Updates slider to requested PWM level.
                | on_slider_change - Handles slider drag callback.
                | set_enabled - Enables or disables slider widget.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def get_speed(self) -> int:
        '''
            Returns current PWM speed integer value.

            :return: Speed integer in range [0, 255].
        '''

    def set_speed(self, speed: int) -> None:
        '''
            Updates slider to requested PWM level.

            :param speed: New PWM speed integer.
        '''

    def on_slider_change(self, value: str) -> None:
        '''
            Handles slider drag interaction.

            :param value: Scale value string from Tkinter callback.
        '''

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables speed slider control.

            :param enabled: True if interactive, False otherwise.
        '''
