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
    Provides ConsoleToolbarSection with clear and copy controls.
'''

from __future__ import annotations

from tkinter import LEFT, RIGHT, X, Tk
from tkinter.ttk import Button, Frame, Label
from typing import ClassVar

from botracked.infrastructure.gui.console.stream.isection import IConsoleStreamSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsoleToolbarSection:
    '''
        Defines class ConsoleToolbarSection implementing IConsoleToolbarSection.
        Leaf GUI component hosting header title and log control action buttons.

        It defines:

            :attributes:
                | HEADER_TEXT - Console header title label.
                | BTN_WIDTH - Action button character width.
                | BTN_PADX - Horizontal padding around action buttons.
                | PADDING - Toolbar internal frame padding tuple.
                | _frame - Root Frame widget.
                | _stream_section - Target console stream section port.
            :methods:
                | __init__ - Initializes toolbar header and action buttons.
                | get_widget - Returns root Frame widget.
                | on_clear - Clears target stream content.
                | on_copy - Copies target stream content to clipboard.
    '''

    HEADER_TEXT: ClassVar[str] = 'BINARY PROTOCOL PACKET STREAM'
    BTN_WIDTH: ClassVar[int] = 8
    BTN_PADX: ClassVar[int] = 2
    PADDING: ClassVar[tuple[int, int]] = (8, 4)

    _frame: Frame
    _stream_section: IConsoleStreamSection

    def __init__(
        self, parent: Tk | Frame, stream_section: IConsoleStreamSection
    ) -> None:
        '''
            Initializes toolbar header and action buttons.

            :param parent: Parent Tk widget.
            :param stream_section: Target console stream section port.
            :exceptions: None.
        '''
        self._frame = Frame(
            parent, style='Surface.TFrame', padding=self.PADDING
        )
        self._stream_section = stream_section

        btn_clear = Button(
            self._frame,
            text='Clear',
            width=self.BTN_WIDTH,
            command=self.on_clear,
        )
        btn_clear.pack(side=RIGHT, padx=self.BTN_PADX)

        btn_copy = Button(
            self._frame,
            text='Copy',
            width=self.BTN_WIDTH,
            command=self.on_copy,
        )
        btn_copy.pack(side=RIGHT, padx=self.BTN_PADX)

        lbl = Label(
            self._frame,
            text=self.HEADER_TEXT,
            style='SurfaceHeader.TLabel',
            anchor='w',
        )
        lbl.pack(side=LEFT, fill=X, expand=True, padx=4)

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def on_clear(self) -> None:
        '''
            Clears target stream content.

            :exceptions: None.
        '''
        self._stream_section.clear()

    def on_copy(self) -> None:
        '''
            Copies target stream content to clipboard.

            :exceptions: None.
        '''
        self._stream_section.copy_selection()
