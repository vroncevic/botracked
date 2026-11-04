# -*- coding: UTF-8 -*-

'''
Module
    icursor.py
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
    Defines ITokenCursor structural protocol for sequential token navigation.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, Self, runtime_checkable

from botracked.core.model.dsl.token import Token

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITokenCursor(Protocol):
    '''
        Defines structural protocol ITokenCursor for sequential token streams.

        It defines:

            :methods:
                | open - Creates isolated token cursor positioned at stream start.
                | current - Returns token at current cursor position.
                | advance - Advances position and returns previous token.
                | is_at_end - Checks if cursor reached end of token stream.
                | skip_newlines - Skips consecutive newline tokens.
    '''

    def open(self, tokens: Sequence[Token]) -> Self:
        '''
            Creates an isolated token cursor bound to given token sequence.

            :param tokens: Sequence of lexical tokens.
            :return: Isolated cursor positioned at index zero.
        '''

    def current(self) -> Token:
        '''
            Returns token at current cursor position.

            :return: Current Token instance.
        '''

    def advance(self) -> Token:
        '''
            Advances position and returns token before increment.

            :return: Token instance at position before increment.
        '''

    def is_at_end(self) -> bool:
        '''
            Checks if cursor reached end of token stream.

            :return: True if EOF reached or stream exhausted, False otherwise.
        '''

    def skip_newlines(self) -> None:
        '''
            Skips consecutive newline tokens.
        '''
