# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Provides ConsolePanel composite coordinating live stream and toolbar.
'''

from __future__ import annotations

from tkinter import BOTH, TOP, X
from tkinter.ttk import Frame
from typing import ClassVar

from botracked.infrastructure.gui.console.stream.isection import IConsoleStreamSection
from botracked.infrastructure.gui.console.toolbar.isection import IConsoleToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsolePanel:
    '''
        Defines class ConsolePanel implementing IConsolePanel, ILogListener,
        and IPacketStreamSink contracts structurally.

        It defines:

            :attributes:
                | TOOLBAR_GAP - Vertical spacing below toolbar section.
                | _frame - Root Frame widget.
                | _stream_section - Injected stream viewer leaf section port.
                | _toolbar_section - Injected toolbar controls leaf section port.
            :methods:
                | __init__ - Initializes console panel with injected sections.
                | get_widget - Returns root Frame widget.
                | write_entry - Appends log entry with level tag to stream.
                | append_packet - Appends binary protocol packet trace.
                | clear - Clears all stream text content.
                | copy_selection - Copies selected or all text to clipboard.
    '''

    TOOLBAR_GAP: ClassVar[int] = 4

    _frame: Frame
    _stream_section: IConsoleStreamSection
    _toolbar_section: IConsoleToolbarSection

    def __init__(
        self,
        frame: Frame,
        stream_section: IConsoleStreamSection,
        toolbar_section: IConsoleToolbarSection,
    ) -> None:
        '''
            Initializes console panel and mounts injected child sections.

            :param frame: Root container Frame widget.
            :param stream_section: Injected console stream leaf section.
            :param toolbar_section: Injected console toolbar leaf section.
            :exceptions: None.
        '''
        self._frame = frame
        self._stream_section = stream_section
        self._toolbar_section = toolbar_section

        self._toolbar_section.get_widget().pack(
            in_=self._frame, fill=X, side=TOP, pady=(0, self.TOOLBAR_GAP)
        )
        self._stream_section.get_widget().pack(
            in_=self._frame, fill=BOTH, expand=True
        )

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def write_entry(self, level: str, message: str) -> None:
        '''
            Appends log entry with level tag to stream.

            :param level: Severity label string.
            :param message: Log text content.
            :exceptions: None.
        '''
        self._stream_section.write_entry(level, message)

    def append_packet(
        self, direction: str, opcode_name: str, raw_hex: str
    ) -> None:
        '''
            Appends binary protocol packet trace to stream.

            :param direction: Direction string ('TX' or 'RX').
            :param opcode_name: Opcode mnemonic label.
            :param raw_hex: Hex string representation of wire bytes.
            :exceptions: None.
        '''
        self._stream_section.append_packet(direction, opcode_name, raw_hex)

    def clear(self) -> None:
        '''
            Clears all stream text content.

            :exceptions: None.
        '''
        self._stream_section.clear()

    def copy_selection(self) -> None:
        '''
            Copies selected or all text content to clipboard.

            :exceptions: None.
        '''
        self._stream_section.copy_selection()
