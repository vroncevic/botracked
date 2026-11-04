# -*- coding: UTF-8 -*-

'''
Module
    highlighter.py
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
    Provides MissionSyntaxHighlighter coordinating buffer-wide DSL styling.
'''

from __future__ import annotations

from tkinter import END, Text
from typing import ClassVar

from botracked.infrastructure.gui.mission.syntax.config import MissionSyntaxConfig
from botracked.infrastructure.gui.mission.syntax.matcher.imatcher import IMissionSyntaxMatcher
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionSyntaxHighlighter:
    '''
        Defines class MissionSyntaxHighlighter implementing
        IMissionSyntaxHighlighter contract structurally.

        It defines:

            :attributes:
                | START_IDX - Buffer start index token for Tkinter Text.
                | END_LINE_TRIM - Trailing newline trim index token.
                | _config - Syntax configuration value object.
                | _matcher - Injected line syntax matcher port.
            :methods:
                | __init__ - Initializes highlighter with config and matcher.
                | setup_tags - Configures color and font tags on Text widget.
                | apply_highlight - Re-highlights entire Text widget buffer.
    '''

    START_IDX: ClassVar[str] = '1.0'
    END_LINE_TRIM: ClassVar[str] = 'end-1c'

    _config: MissionSyntaxConfig
    _matcher: IMissionSyntaxMatcher

    def __init__(
        self,
        config: MissionSyntaxConfig,
        matcher: IMissionSyntaxMatcher,
    ) -> None:
        '''
            Initializes highlighter with syntax configuration and line matcher.

            :param config: Syntax highlighting configuration value object.
            :param matcher: Injected line syntax matcher contract.
            :exceptions: None.
        '''
        self._config = config
        self._matcher = matcher

    def setup_tags(self, text_widget: Text) -> None:
        '''
            Configures color and font tags on target Text widget.

            :param text_widget: Target Tkinter Text widget.
            :exceptions: None.
        '''
        cfg = self._config
        text_widget.tag_configure(
            cfg.tag_comment, foreground=UIColors.TEXT_DIM
        )
        text_widget.tag_configure(
            cfg.tag_keyword, foreground=UIColors.CYAN, font=cfg.font_bold
        )
        text_widget.tag_configure(
            cfg.tag_control, foreground=UIColors.PURPLE, font=cfg.font_bold
        )
        text_widget.tag_configure(cfg.tag_number, foreground=UIColors.AMBER)

    def apply_highlight(self, text_widget: Text) -> None:
        '''
            Clears stale tags and highlights all lines in Text widget buffer.

            :param text_widget: Target Tkinter Text widget.
            :exceptions: None.
        '''
        cfg = self._config
        for tag in (
            cfg.tag_comment,
            cfg.tag_keyword,
            cfg.tag_control,
            cfg.tag_number,
        ):
            text_widget.tag_remove(tag, self.START_IDX, END)

        content: str = text_widget.get(self.START_IDX, self.END_LINE_TRIM)
        for idx, line in enumerate(content.splitlines(), start=1):
            self._matcher.highlight_line(text_widget, idx, line)
