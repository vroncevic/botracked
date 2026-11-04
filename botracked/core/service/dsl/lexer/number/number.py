# -*- coding: UTF-8 -*-

'''
Module
    number.py
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
    Defines NumberScanner scanning numeric literal tokens from script text lines.
'''

from __future__ import annotations

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


class NumberScanner:
    '''
        Defines class NumberScanner implementing INumberScanner structurally.
        Extracts integer and floating-point numeric tokens from line characters.

        It defines:

            :attributes:
                | DECIMAL_POINT - Decimal separator character for float literals.
            :methods:
                | __init__ - Initializes number scanner.
                | is_number_start - Checks if character starts a number literal.
                | scan - Scans numerical literal and returns token with column.
    '''

    DECIMAL_POINT: ClassVar[str] = '.'

    def __init__(self) -> None:
        '''
            Initializes number scanner.

            :exceptions: None.
        '''

    def is_number_start(self, ch: str, col: int, line: str) -> bool:
        '''
            Checks if character sequence starts a number literal.

            :param ch: Character under current column.
            :param col: Column index (1-based).
            :param line: Complete text line.
            :return: True if number starts here, False otherwise.
            :exceptions: None.
        '''
        return ch.isdigit() or (
            ch == self.DECIMAL_POINT and col < len(line) and line[col].isdigit()
        )

    def scan(self, line: str, col: int, line_idx: int) -> tuple[Token, int]:
        '''
            Scans a numerical literal and returns token with advanced column.

            :param line: Source text line.
            :param col: Starting column index (1-based).
            :param line_idx: Line number (1-based).
            :return: Tuple of generated Token and updated column index.
            :exceptions: None.
        '''
        start_col: int = col
        num_str: str = ''
        has_dot: bool = False
        length: int = len(line)

        while col <= length and (
            line[col - 1].isdigit() or line[col - 1] == self.DECIMAL_POINT
        ):
            if line[col - 1] == self.DECIMAL_POINT:
                if has_dot:
                    break
                has_dot = True

            num_str += line[col - 1]
            col += 1

        return Token(TokenType.NUMBER, num_str, line_idx, start_col), col
