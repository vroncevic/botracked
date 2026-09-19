# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_highlighter.py
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
    Provides DslSyntaxHighlighter for real-time .track code syntax highlighting.
'''

from __future__ import annotations

from re import Pattern, compile as re_compile
from tkinter import Text

from botracked.infrastructure.gui.editor.dsl_syntax_highlighter_config import (
    DslSyntaxHighlighterConfig,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslSyntaxHighlighter:
    '''
        Defines class DslSyntaxHighlighter with attribute(s) and method(s).
        Applies syntax coloring to .track mission scripts in Tkinter Text widget.

        It defines:

            :attributes:
                | _config - Configuration parameters for syntax highlighting.
                | _pat_keyword - Compiled regex pattern for action keywords.
                | _pat_control - Compiled regex pattern for control keywords.
                | _pat_number - Compiled regex pattern for numeric literals.
            :methods:
                | __init__ - Initializes highlighter and compiles regex patterns.
                | setup_tags - Configures syntax highlight tags on Text widget.
                | apply_highlight - Scans and colorizes full text content.
    '''

    _config: DslSyntaxHighlighterConfig
    _pat_keyword: Pattern[str]
    _pat_control: Pattern[str]
    _pat_number: Pattern[str]

    def __init__(
        self, config: DslSyntaxHighlighterConfig | None = None
    ) -> None:
        '''
            Initializes highlighter and compiles regex patterns.

            :param config: Optional highlighter configuration instance.
            :type config: DslSyntaxHighlighterConfig | None

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        self._config = (
            config if config is not None else DslSyntaxHighlighterConfig()
        )
        self._pat_keyword = re_compile(self._config.pattern_keyword)
        self._pat_control = re_compile(self._config.pattern_control)
        self._pat_number = re_compile(self._config.pattern_number)

    def setup_tags(self, text_widget: Text) -> None:
        '''
            Configures syntax highlight tags on Text widget.

            :param text_widget: Tkinter Text widget to style.
            :type text_widget: Text

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        cfg: DslSyntaxHighlighterConfig = self._config
        text_widget.tag_configure(
            cfg.tag_keyword,
            foreground=cfg.color_keyword,
            font=('Consolas', 10, 'bold'),
        )
        text_widget.tag_configure(
            cfg.tag_control,
            foreground=cfg.color_control,
            font=('Consolas', 10, 'bold'),
        )
        text_widget.tag_configure(
            cfg.tag_number,
            foreground=cfg.color_number,
        )
        text_widget.tag_configure(
            cfg.tag_comment,
            foreground=cfg.color_comment,
            font=('Consolas', 10, 'italic'),
        )

    def apply_highlight(self, text_widget: Text) -> None:
        '''
            Scans and colorizes full text content of widget.

            :param text_widget: Tkinter Text widget to highlight.
            :type text_widget: Text

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        cfg: DslSyntaxHighlighterConfig = self._config
        for tag in (
            cfg.tag_keyword,
            cfg.tag_control,
            cfg.tag_number,
            cfg.tag_comment,
        ):
            text_widget.tag_remove(tag, '1.0', 'end')

        content: str = text_widget.get('1.0', 'end-1c')
        for line_idx, line in enumerate(content.splitlines(), start=1):
            self._highlight_line(text_widget, line, line_idx)

    def _match_and_tag(
        self,
        text_widget: Text,
        line: str,
        line_idx: int,
        rule: tuple[Pattern[str], str],
    ) -> None:
        '''
            Matches pattern against line slice and applies tag.

            :param text_widget: Text widget being formatted.
            :param line: Text line slice to inspect.
            :param line_idx: 1-based line index.
            :param rule: Tuple of (compiled pattern, tag name).
            :exceptions: None.
        '''
        pattern, tag = rule
        for match in pattern.finditer(line):
            start_col, end_col = match.span()
            text_widget.tag_add(
                tag, f'{line_idx}.{start_col}', f'{line_idx}.{end_col}'
            )

    def _highlight_line(
        self, text_widget: Text, line: str, line_idx: int
    ) -> None:
        '''
            Highlights single line distinguishing code and comments.

            :param text_widget: Target Text widget.
            :param line: Line text content.
            :param line_idx: 1-based line number.
            :exceptions: None.
        '''
        comment_idx: int = line.find('#')
        effective_line: str = line if comment_idx == -1 else line[:comment_idx]

        rules: tuple[tuple[Pattern[str], str], ...] = (
            (self._pat_keyword, self._config.tag_keyword),
            (self._pat_control, self._config.tag_control),
            (self._pat_number, self._config.tag_number),
        )
        for rule in rules:
            self._match_and_tag(text_widget, effective_line, line_idx, rule)

        if comment_idx != -1:
            start_pos: str = f'{line_idx}.{comment_idx}'
            end_pos: str = f'{line_idx}.{len(line)}'
            text_widget.tag_add(self._config.tag_comment, start_pos, end_pos)
