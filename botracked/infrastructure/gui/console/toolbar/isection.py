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
    Defines IConsoleToolbarSection protocol for console clear/copy controls.
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
class IConsoleToolbarSection(Protocol):
    '''
        Defines structural contract IConsoleToolbarSection for console header.

        It defines:

            :methods:
                | get_widget - Returns root Frame widget.
                | on_clear - Clears target console stream content.
                | on_copy - Copies target console stream content to clipboard.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
        '''

    def on_clear(self) -> None:
        '''
            Clears target console stream content.
        '''

    def on_copy(self) -> None:
        '''
            Copies target console stream content to clipboard.
        '''
