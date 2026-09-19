# -*- coding: UTF-8 -*-

'''
Module
    itbot_lexer.py
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
    Defines ITbotLexer interface for tokenizing .track mission scripts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.token import Token

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITbotLexer(Protocol):
    '''
        Defines protocol ITbotLexer with method(s).
        Protocol for lexical scanner transforming source code into tokens.

        It defines:

            :methods:
                | tokenize - Scans source code and generates a list of tokens.
                | count_tokens - Scans source code and returns total token count.
    '''

    def tokenize(self, source: str) -> list[Token]:
        '''
            Scans source code and generates a list of tokens.

            :param source: Raw text content of .track script.
            :return: List of Token objects ending with EOF token.
        '''

    def count_tokens(self, source: str) -> int:
        '''
            Scans source code and returns total number of lexical tokens.

            :param source: Raw text content of .track script.
            :return: Integer count of tokens including EOF.
        '''
