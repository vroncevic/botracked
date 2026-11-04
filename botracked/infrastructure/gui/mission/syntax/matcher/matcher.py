# -*- coding: UTF-8 -*-

'''
Module
    matcher.py
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
    Provides MissionSyntaxMatcher applying regex tags to editor lines.
'''

from __future__ import annotations

from re import IGNORECASE, compile as re_compile
from tkinter import Text

from botracked.infrastructure.gui.mission.syntax.config import MissionSyntaxConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionSyntaxMatcher:
    '''
        Defines class MissionSyntaxMatcher implementing IMissionSyntaxMatcher.
        Matches DSL comments, command keywords, loop blocks, and numeric tokens.

        It defines:

            :attributes:
                | _config - Syntax highlighting configuration value object.
            :methods:
                | __init__ - Initializes matcher with syntax configuration.
                | match_and_tag - Applies regex tag across a single line.
                | highlight_line - Highlights tokens on a single editor line.
    '''

    _config: MissionSyntaxConfig

    def __init__(self, config: MissionSyntaxConfig) -> None:
        '''
            Initializes matcher with syntax configuration.

            :param config: Syntax highlighting configuration value object.
            :exceptions: None.
        '''
        self._config = config

    def match_and_tag(
        self,
        text_widget: Text,
        pattern_str: str,
        tag_name: str,
        line_spec: tuple[int, str],
    ) -> None:
        '''
            Applies regex pattern tag across a single editor line.

            :param text_widget: Target Tkinter Text widget.
            :param pattern_str: Regular expression string.
            :param tag_name: Tag identifier applied to matched spans.
            :param line_spec: Tuple of 1-based line index and line text.
            :exceptions: None.
        '''
        line_idx, line_content = line_spec
        compiled = re_compile(pattern_str, IGNORECASE)
        for match in compiled.finditer(line_content):
            start_pos: str = f'{line_idx}.{match.start()}'
            end_pos: str = f'{line_idx}.{match.end()}'
            text_widget.tag_add(tag_name, start_pos, end_pos)

    def highlight_line(
        self, text_widget: Text, line_idx: int, line_content: str
    ) -> None:
        '''
            Highlights comments, keywords, control blocks, and numbers on line.

            :param text_widget: Target Tkinter Text widget.
            :param line_idx: 1-based line index in Text widget.
            :param line_content: Raw string content of target line.
            :exceptions: None.
        '''
        cfg = self._config
        stripped: str = line_content.lstrip()
        if stripped.startswith(cfg.comment_prefix):
            text_widget.tag_add(
                cfg.tag_comment,
                f'{line_idx}.0',
                f'{line_idx}.{len(line_content)}',
            )
            return

        spec: tuple[int, str] = (line_idx, line_content)
        self.match_and_tag(
            text_widget, cfg.pattern_keyword, cfg.tag_keyword, spec
        )
        self.match_and_tag(
            text_widget, cfg.pattern_control, cfg.tag_control, spec
        )
        self.match_and_tag(
            text_widget, cfg.pattern_number, cfg.tag_number, spec
        )
