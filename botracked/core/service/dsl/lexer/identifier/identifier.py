# -*- coding: UTF-8 -*-

'''
Module
    identifier.py
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
    Defines IdentifierScanner scanning keywords and identifiers from script lines.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IdentifierScanner:
    '''
        Defines class IdentifierScanner implementing IIdentifierScanner.
        Extracts keywords and generic identifier tokens from line characters.

        It defines:

            :attributes:
                | UNDERSCORE - Underscore character allowed in identifiers.
                | _KEYWORDS - Immutable mapping of reserved words to TokenType.
            :methods:
                | __init__ - Initializes identifier scanner.
                | is_identifier_start - Checks if character starts an identifier.
                | scan - Scans an identifier or keyword from line.
    '''

    UNDERSCORE: ClassVar[str] = '_'
    _KEYWORDS: ClassVar[MappingProxyType[str, TokenType]] = MappingProxyType({
        'SPEED': TokenType.SPEED,
        'FORWARD': TokenType.FORWARD,
        'BACKWARD': TokenType.BACKWARD,
        'TURN_LEFT': TokenType.TURN_LEFT,
        'TURN_RIGHT': TokenType.TURN_RIGHT,
        'SPIN_LEFT': TokenType.SPIN_LEFT,
        'SPIN_RIGHT': TokenType.SPIN_RIGHT,
        'WAIT': TokenType.WAIT,
        'STOP': TokenType.STOP,
        'PING': TokenType.PING,
        'CLEAR_ERRORS': TokenType.CLEAR_ERRORS,
        'REPEAT': TokenType.REPEAT,
        'END': TokenType.END,
    })

    def __init__(self) -> None:
        '''
            Initializes identifier scanner.

            :exceptions: None.
        '''

    def is_identifier_start(self, ch: str) -> bool:
        '''
            Checks if character starts an identifier or keyword.

            :param ch: Character under current column.
            :return: True if alphabetical or underscore, False otherwise.
            :exceptions: None.
        '''
        return ch.isalpha() or ch == self.UNDERSCORE

    def scan(self, line: str, col: int, line_idx: int) -> tuple[Token, int]:
        '''
            Scans an identifier or keyword and returns token with advanced column.

            :param line: Source text line.
            :param col: Starting column index (1-based).
            :param line_idx: Line number (1-based).
            :return: Tuple of generated Token and updated column index.
            :exceptions: None.
        '''
        start_col: int = col
        ident: str = ''
        length: int = len(line)

        while col <= length and (
            line[col - 1].isalnum() or line[col - 1] == self.UNDERSCORE
        ):
            ident += line[col - 1]
            col += 1

        tok_type: TokenType = self._KEYWORDS.get(
            ident.upper(), TokenType.IDENTIFIER
        )

        return Token(tok_type, ident, line_idx, start_col), col
