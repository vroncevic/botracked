# -*- coding: UTF-8 -*-

'''
Module
    cursor.py
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
    Defines TokenCursor managing isolated traversal over lexical Token streams.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Self

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


class TokenCursor:
    '''
        Defines class TokenCursor implementing ITokenCursor structurally.
        Encapsulates isolated position index over an immutable token tuple.

        It defines:

            :attributes:
                | INITIAL_POS - Starting 0-based position in token sequence.
                | DEFAULT_LINE - Default line index for empty stream EOF token.
                | DEFAULT_COL - Default column index for empty stream EOF token.
                | _tokens - Immutable sequence of tokens.
                | _pos - Current traversal position.
            :methods:
                | __init__ - Initializes token cursor over given sequence.
                | open - Creates isolated token cursor positioned at stream start.
                | current - Returns token at current cursor position.
                | advance - Advances position and returns current token.
                | is_at_end - Checks if cursor reached end of tokens.
                | skip_newlines - Skips consecutive newline tokens.
    '''

    INITIAL_POS: ClassVar[int] = 0
    DEFAULT_LINE: ClassVar[int] = 1
    DEFAULT_COL: ClassVar[int] = 1

    _tokens: tuple[Token, ...]
    _pos: int

    def __init__(self, tokens: Sequence[Token]) -> None:
        '''
            Initializes token cursor at initial position over defensive copy.

            :param tokens: Sequence of lexical tokens.
            :exceptions: None.
        '''
        self._tokens = tuple(tokens)
        self._pos = self.INITIAL_POS

    def open(self, tokens: Sequence[Token]) -> Self:
        '''
            Creates an isolated token cursor bound to given token sequence.

            :param tokens: Sequence of lexical tokens.
            :return: Isolated TokenCursor instance positioned at index zero.
            :exceptions: None.
        '''
        return type(self)(tokens)

    def current(self) -> Token:
        '''
            Returns token at current cursor position or EOF sentinel token.

            :return: Current Token instance.
            :exceptions: None.
        '''
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]

        if self._tokens:
            return self._tokens[-1]

        return Token(TokenType.EOF, '', self.DEFAULT_LINE, self.DEFAULT_COL)

    def advance(self) -> Token:
        '''
            Advances position and returns current token before advancement.

            :return: Token instance at position before increment.
            :exceptions: None.
        '''
        tok: Token = self.current()

        if not self.is_at_end():
            self._pos += 1

        return tok

    def is_at_end(self) -> bool:
        '''
            Checks if cursor reached end of tokens.

            :return: True if EOF reached or stream exhausted, False otherwise.
            :exceptions: None.
        '''
        if self._pos >= len(self._tokens):
            return True

        return self.current().token_type == TokenType.EOF

    def skip_newlines(self) -> None:
        '''
            Skips consecutive newline tokens.

            :exceptions: None.
        '''
        while not self.is_at_end() and self.current().token_type == TokenType.NEWLINE:
            self.advance()
