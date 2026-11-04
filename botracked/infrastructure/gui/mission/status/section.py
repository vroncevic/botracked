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
    Provides MissionStatusSection leaf UI component for mission feedback.
'''

from __future__ import annotations

from tkinter import LEFT, X, StringVar, Tk
from tkinter.ttk import Frame, Label
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

class MissionStatusSection:
    '''
        Defines class MissionStatusSection implementing IMissionStatusSection
        contract structurally.

        It defines:

            :attributes:
                | INITIAL_TEXT - Default status indicator caption.
                | LABEL_PADX - Horizontal padding around status label.
                | _frame - Section container Frame widget.
                | _status_var - Bound StringVar holding status text.
                | _label - Tkinter ttk Label displaying status message.
            :methods:
                | __init__ - Initializes status indicator leaf section.
                | get_widget - Returns section container Frame widget.
                | set_status - Updates status text and foreground color.
                | get_status_text - Returns current status message text.
    '''

    INITIAL_TEXT: ClassVar[str] = 'Ready'
    LABEL_PADX: ClassVar[int] = 4

    _frame: Frame
    _status_var: StringVar
    _label: Label

    def __init__(self, parent: Frame | Tk) -> None:
        '''
            Initializes status indicator leaf section.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Panel.TFrame')
        self._status_var = StringVar(value=self.INITIAL_TEXT)
        self._label = Label(
            self._frame,
            textvariable=self._status_var,
            style='Panel.TLabel',
            foreground=UIColors.TEXT_MUTED,
            anchor='w',
        )
        self._label.pack(side=LEFT, fill=X, expand=True, padx=self.LABEL_PADX)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def set_status(self, message: str, fg_color: str) -> None:
        '''
            Updates status message text and foreground color.

            :param message: Status message text.
            :param fg_color: Foreground color hex string.
            :exceptions: None.
        '''
        self._status_var.set(message)
        self._label.configure(foreground=fg_color)

    def get_status_text(self) -> str:
        '''
            Returns current status message text.

            :return: Status message string.
            :exceptions: None.
        '''
        return self._status_var.get()
