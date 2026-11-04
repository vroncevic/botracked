# -*- coding: UTF-8 -*-

'''
Module
    config.py
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
    Provides MissionSyntaxConfig immutable DSL highlighting configuration.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class MissionSyntaxConfig:
    '''
        Immutable configuration for DSL syntax highlighting tags and patterns.

        It defines:

            :attributes:
                | tag_comment - Tag identifier for comments.
                | tag_keyword - Tag identifier for DSL command keywords.
                | tag_control - Tag identifier for repeat loop controls.
                | tag_number - Tag identifier for numeric literals.
                | pattern_keyword - Regex pattern matching DSL keywords.
                | pattern_control - Regex pattern matching loop keywords.
                | pattern_number - Regex pattern matching numeric literals.
                | comment_prefix - Character prefix marking comment lines.
                | font_bold - Bold monospace font specification.
    '''

    tag_comment: str = 'comment'
    tag_keyword: str = 'keyword'
    tag_control: str = 'control'
    tag_number: str = 'number'
    pattern_keyword: str = (
        r'\b(SPEED|FORWARD|BACKWARD|TURN_LEFT|TURN_RIGHT|'
        r'SPIN_LEFT|SPIN_RIGHT|STOP|WAIT|PING|CLEAR_ERRORS)\b'
    )
    pattern_control: str = r'\b(REPEAT|END)\b'
    pattern_number: str = r'\b\d+(\.\d+)?\b'
    comment_prefix: str = '#'
    font_bold: tuple[str, int, str] = ('Courier', 10, 'bold')
