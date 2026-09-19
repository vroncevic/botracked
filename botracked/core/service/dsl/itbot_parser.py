# -*- coding: UTF-8 -*-

'''
Module
    itbot_parser.py
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
    Defines ITbotParser interface for parsing tokens into an AST instruction list.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
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
class ITbotParser(Protocol):
    '''
        Defines protocol ITbotParser with method(s).
        Protocol for parser validating grammar and generating AST instruction nodes.

        It defines:

            :methods:
                | parse - Parses token stream into abstract syntax tree nodes.
                | validate_syntax - Validates token sequence without exceptions.
    '''

    def parse(self, tokens: list[Token]) -> list[AstInstruction]:
        '''
            Parses token stream into abstract syntax tree instructions.

            :param tokens: List of lexical tokens from lexer.
            :return: List of AstInstruction nodes.
        '''

    def validate_syntax(self, tokens: list[Token]) -> tuple[bool, str]:
        '''
            Validates token sequence without throwing exceptions.

            :param tokens: List of lexical tokens to validate.
            :return: Tuple of (is_valid, error_message).
        '''
