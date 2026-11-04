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
    Defines IMissionStatusSection protocol for mission status leaf UI.
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
class IMissionStatusSection(Protocol):
    '''
        Defines structural contract IMissionStatusSection for status indicator.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | set_status - Updates status text and foreground color.
                | get_status_text - Returns current status message string.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def set_status(self, message: str, fg_color: str) -> None:
        '''
            Updates status text and foreground color.

            :param message: Status message text.
            :param fg_color: Foreground color hex string.
        '''

    def get_status_text(self) -> str:
        '''
            Returns current status message string.

            :return: Status text string.
        '''
