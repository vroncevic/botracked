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
    Provides MissionEditorSection leaf UI component for DSL script editing.
'''

from __future__ import annotations

from tkinter import BOTH, END, LEFT, RIGHT, VERTICAL, Y, Text, Tk
from tkinter.ttk import Frame, Scrollbar
from typing import ClassVar

from botracked.infrastructure.gui.mission.syntax.highlighter.ihighlighter import IMissionSyntaxHighlighter
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionEditorSection:
    '''
        Defines class MissionEditorSection implementing IMissionEditorSection
        contract structurally.

        It defines:

            :attributes:
                | START_IDX - Buffer start index token for Tkinter Text.
                | END_TRIM - Trailing newline trim index token.
                | KEY_RELEASE_EVENT - Tkinter event sequence for key release.
                | EDITOR_FONT - Monospace font tuple for DSL editor.
                | EDITOR_PAD - Inner pixel padding for Text widget.
                | EDITOR_WIDTH - Initial character width of Text widget.
                | EDITOR_HEIGHT - Initial line height of Text widget.
                | _frame - Section container Frame widget.
                | _highlighter - Injected DSL syntax highlighter port.
                | _editor - Tkinter Text widget hosting .track script.
            :methods:
                | __init__ - Initializes editor widget, scrollbar, and tags.
                | get_widget - Returns section container Frame widget.
                | get_script - Returns raw script text from editor buffer.
                | set_script - Replaces editor buffer and highlights syntax.
                | on_key_release - Handles key release to refresh syntax tags.
    '''

    START_IDX: ClassVar[str] = '1.0'
    END_TRIM: ClassVar[str] = 'end-1c'
    KEY_RELEASE_EVENT: ClassVar[str] = '<KeyRelease>'
    EDITOR_FONT: ClassVar[tuple[str, int]] = ('DejaVu Sans Mono', 9)
    EDITOR_PAD: ClassVar[int] = 8
    EDITOR_WIDTH: ClassVar[int] = 56
    EDITOR_HEIGHT: ClassVar[int] = 16

    _frame: Frame
    _highlighter: IMissionSyntaxHighlighter
    _editor: Text

    def __init__(
        self,
        parent: Frame | Tk,
        highlighter: IMissionSyntaxHighlighter,
    ) -> None:
        '''
            Initializes editor widget, vertical scrollbar, and syntax tags.

            :param parent: Parent container widget.
            :param highlighter: Injected DSL syntax highlighter contract.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Surface.TFrame')
        self._highlighter = highlighter
        self._editor = Text(
            self._frame,
            width=self.EDITOR_WIDTH,
            height=self.EDITOR_HEIGHT,
            background=UIColors.BG_DARK,
            foreground=UIColors.TEXT_MAIN,
            insertbackground=UIColors.CYAN,
            highlightthickness=1,
            highlightbackground=UIColors.BORDER,
            highlightcolor=UIColors.CYAN,
            font=self.EDITOR_FONT,
            relief='flat',
            padx=self.EDITOR_PAD,
            pady=self.EDITOR_PAD,
            undo=True,
        )
        scrollbar = Scrollbar(
            self._frame, orient=VERTICAL, command=self._editor.yview
        )
        self._editor.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self._editor.pack(side=LEFT, fill=BOTH, expand=True)

        self._highlighter.setup_tags(self._editor)
        self._editor.bind(self.KEY_RELEASE_EVENT, self.on_key_release)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_script(self) -> str:
        '''
            Returns raw script text from editor buffer.

            :return: Raw .track script string.
            :exceptions: None.
        '''
        return self._editor.get(self.START_IDX, self.END_TRIM)

    def set_script(self, text: str) -> None:
        '''
            Replaces editor buffer and applies syntax highlighting.

            :param text: Raw .track script string.
            :exceptions: None.
        '''
        self._editor.delete(self.START_IDX, END)
        self._editor.insert(self.START_IDX, text)
        self._highlighter.apply_highlight(self._editor)

    def on_key_release(self, event: object) -> None:
        '''
            Handles key release event to refresh syntax highlighting.

            :param event: Tkinter KeyRelease event object.
            :exceptions: None.
        '''
        _ = event
        self._highlighter.apply_highlight(self._editor)
