# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_highlighter_config.py
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
    Configuration dataclass holding tag names, colors, and regexes for DSL highlighter.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class DslSyntaxHighlighterConfig:
    '''
        Defines class DslSyntaxHighlighterConfig with attribute(s) and method(s).
        Configuration parameters for mission script syntax highlighting.

        It defines:

            :attributes:
                | tag_keyword - Tag name for command keywords.
                | tag_control - Tag name for control flow keywords.
                | tag_number - Tag name for numeric literals.
                | tag_comment - Tag name for comment lines.
                | color_keyword - Highlight foreground color for command keywords.
                | color_control - Highlight foreground color for control keywords.
                | color_number - Highlight foreground color for numbers.
                | color_comment - Highlight foreground color for comments.
                | pattern_keyword - Regex pattern matching action keywords.
                | pattern_control - Regex pattern matching loop and wait keywords.
                | pattern_number - Regex pattern matching numeric literals.
                | pattern_comment - Regex pattern matching line comments.
    '''

    tag_keyword: str = 'keyword'
    tag_control: str = 'control'
    tag_number: str = 'number'
    tag_comment: str = 'comment'

    color_keyword: str = UIColors.CYAN
    color_control: str = UIColors.GREEN
    color_number: str = UIColors.AMBER
    color_comment: str = UIColors.TEXT_MUTED

    pattern_keyword: str = (
        r'\b(SPEED|FORWARD|BACKWARD|TURN_LEFT|TURN_RIGHT|'
        r'SPIN_LEFT|SPIN_RIGHT|STOP|PING|CLEAR_ERRORS)\b'
    )
    pattern_control: str = r'\b(REPEAT|END|WAIT)\b'
    pattern_number: str = r'\b\d+(\.\d+)?\b'
    pattern_comment: str = r'#.*$'
