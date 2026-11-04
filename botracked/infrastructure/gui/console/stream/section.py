# -*- coding: UTF-8 -*-

'''
Module
    section.py
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
    Provides ConsoleStreamSection scrollable text widget for packet logs.
'''

from __future__ import annotations

from datetime import datetime
from tkinter import BOTH, END, LEFT, RIGHT, VERTICAL, TclError, Text, Tk
from tkinter.ttk import Frame, Scrollbar
from typing import ClassVar

from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsoleStreamSection:
    '''
        Defines class ConsoleStreamSection implementing IConsoleStreamSection.
        Leaf GUI component displaying live binary packet traffic and logs.

        It defines:

            :attributes:
                | STREAM_HEIGHT - Visible line height of console text area.
                | STREAM_PAD - Internal text padding in pixels.
                | STREAM_FONT - Monospace font tuple for packet stream.
                | TIME_FORMAT - Timestamp format string.
                | KNOWN_TAGS - Tuple of recognized color severity tags.
                | _frame - Root Frame widget.
                | _text - Text widget displaying communication packet log.
            :methods:
                | __init__ - Initializes scrolling text stream widget.
                | get_widget - Returns root Frame widget.
                | write_entry - Appends log entry with level tag to stream.
                | append_packet - Appends binary protocol packet trace.
                | clear - Clears all stream text content.
                | copy_selection - Copies selected or all text to clipboard.
    '''

    STREAM_HEIGHT: ClassVar[int] = 16
    STREAM_PAD: ClassVar[int] = 8
    STREAM_FONT: ClassVar[tuple[str, int]] = ('DejaVu Sans Mono', 9)
    TIME_FORMAT: ClassVar[str] = '%H:%M:%S.%f'
    KNOWN_TAGS: ClassVar[tuple[str, ...]] = ('tx', 'rx', 'error', 'warn')

    _frame: Frame
    _text: Text

    def __init__(self, parent: Tk | Frame) -> None:
        '''
            Initializes scrolling text stream widget.

            :param parent: Parent Tk widget.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Panel.TFrame')

        scrollbar = Scrollbar(self._frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill='y')

        self._text = Text(
            self._frame,
            height=self.STREAM_HEIGHT,
            bg=UIColors.BG_DARK,
            fg=UIColors.TEXT_MAIN,
            insertbackground=UIColors.CYAN,
            highlightthickness=1,
            highlightbackground=UIColors.BORDER,
            highlightcolor=UIColors.CYAN,
            font=self.STREAM_FONT,
            yscrollcommand=scrollbar.set,
            relief='flat',
            padx=self.STREAM_PAD,
            pady=self.STREAM_PAD,
            state='disabled',
        )
        self._text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.configure(command=self._text.yview)

        self._text.tag_config('tx', foreground=UIColors.CYAN)
        self._text.tag_config('rx', foreground=UIColors.GREEN)
        self._text.tag_config('error', foreground=UIColors.RED)
        self._text.tag_config('warn', foreground=UIColors.AMBER)
        self._text.tag_config('time', foreground=UIColors.TEXT_DIM)
        self._text.tag_config('hex', foreground=UIColors.AMBER)
        self._text.tag_config('text', foreground=UIColors.TEXT_MAIN)

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
        ts = datetime.now().strftime(self.TIME_FORMAT)[:-3]
        lower_lvl = level.lower()
        tag = lower_lvl if lower_lvl in self.KNOWN_TAGS else 'text'

        self._text.configure(state='normal')
        self._text.insert(END, f'[{ts}] ', 'time')
        self._text.insert(END, f'[{level}] ', tag)
        self._text.insert(END, f'{message}\n', 'text')
        self._text.see(END)
        self._text.configure(state='disabled')

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
        ts = datetime.now().strftime(self.TIME_FORMAT)[:-3]
        tag = 'tx' if direction == 'TX' else 'rx'

        self._text.configure(state='normal')
        self._text.insert(END, f'[{ts}] ', 'time')
        self._text.insert(END, f'[{direction}] ', tag)
        self._text.insert(END, f'{opcode_name:<16} ', tag)
        self._text.insert(END, f'RAW: {raw_hex}\n', 'hex')
        self._text.see(END)
        self._text.configure(state='disabled')

    def clear(self) -> None:
        '''
            Clears all stream text content.

            :exceptions: None.
        '''
        self._text.configure(state='normal')
        self._text.delete('1.0', END)
        self._text.configure(state='disabled')

    def copy_selection(self) -> None:
        '''
            Copies selected or all text content to clipboard.

            :exceptions: None.
        '''
        try:
            content = self._text.get('sel.first', 'sel.last')
        except TclError:
            content = self._text.get('1.0', 'end-1c')
        self._frame.clipboard_clear()
        self._frame.clipboard_append(content)
