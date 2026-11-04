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
    Defines IMissionPanel protocol for composite mission routine studio.
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
class IMissionPanel(Protocol):
    '''
        Defines structural contract IMissionPanel for mission studio composite.

        It defines:

            :methods:
                | get_widget - Returns root container Frame widget.
                | get_script - Returns current DSL script text from editor.
                | set_script - Replaces editor DSL script text.
                | set_status - Updates mission status indicator caption.
                | get_status_text - Returns current mission status caption.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Root Frame widget.
        '''

    def get_script(self) -> str:
        '''
            Returns current DSL script text from editor.

            :return: Raw .track script string.
        '''

    def set_script(self, script: str) -> None:
        '''
            Replaces editor DSL script text.

            :param script: Raw .track script string.
        '''

    def set_status(self, message: str, fg_color: str) -> None:
        '''
            Updates mission status indicator caption and foreground color.

            :param message: Status message text.
            :param fg_color: Foreground color hex string.
        '''

    def get_status_text(self) -> str:
        '''
            Returns current mission status indicator text.

            :return: Status caption string.
        '''
