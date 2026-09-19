# -*- coding: UTF-8 -*-

'''
Module
    token.py
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
    Defines Token value object produced by the mission script lexer.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class Token:
    '''
        Defines Token value object produced by the mission script lexer.
        Immutable lexical token with location metadata for syntax reporting.

        It defines:

            :attributes:
                | token_type - Categorized token type.
                | lexeme - Raw text slice representing the token.
                | value - Parsed literal value or None.
                | line - 1-based source code line number.
                | column - 1-based source code column number.
            :methods:
                | matches - Checks if token matches the given token type.
                | __repr__ - Returns string representation for diagnostics.
    '''

    token_type: TokenType
    lexeme: str
    value: int | float | str | None
    line: int
    column: int

    def matches(self, token_type: TokenType) -> bool:
        '''
            Checks whether token matches the specified token type.

            :param token_type: Token type to compare against.
            :return: True if token type matches, False otherwise.
            :exceptions: None.
        '''
        return self.token_type == token_type

    def __repr__(self) -> str:
        '''
            Returns string representation for diagnostics.

            :return: Diagnostic string representation of token.
            :exceptions: None.
        '''
        return (
            f'Token({self.token_type.name}, lexeme={self.lexeme!r}, '
            f'val={self.value!r}, L{self.line}:C{self.column})'
        )
