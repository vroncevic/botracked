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
    Defines IConsolePanel protocol for packet console composite panel.
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
class IConsolePanel(Protocol):
    '''
        Defines structural contract IConsolePanel for packet stream console.

        It defines:

            :methods:
                | get_widget - Returns root Frame widget.
                | write_entry - Appends severity-tagged log entry.
                | append_packet - Appends binary wire packet trace.
                | clear - Clears all stream text content.
                | copy_selection - Copies selected or full text to clipboard.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
        '''

    def write_entry(self, level: str, message: str) -> None:
        '''
            Appends log entry with level tag to stream.

            :param level: Severity label string.
            :param message: Log text content.
        '''

    def append_packet(
        self, direction: str, opcode_name: str, raw_hex: str
    ) -> None:
        '''
            Appends binary protocol packet trace to stream.

            :param direction: Direction string ('TX' or 'RX').
            :param opcode_name: Opcode mnemonic label.
            :param raw_hex: Hex string representation of wire bytes.
        '''

    def clear(self) -> None:
        '''
            Clears all stream text content.
        '''

    def copy_selection(self) -> None:
        '''
            Copies selected or all text content to clipboard.
        '''
