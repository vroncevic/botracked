# -*- coding: UTF-8 -*-

'''
Module
    parser.py
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
    Defines TbotParser parsing tokens into validated AstInstruction AST nodes.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token import Token
from botracked.core.model.exceptions.dsl_error import DslError
from botracked.core.service.dsl.parser.cursor.icursor import ITokenCursor
from botracked.core.service.dsl.parser.statement.istatement import IStatementParser

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotParser:
    '''
        Defines class TbotParser implementing ITbotParser structurally.
        Recursive descent parser constructing AST from .track token streams.

        It defines:

            :attributes:
                | VALID_MESSAGE - Status message returned when syntax is valid.
                | _cursor - Token cursor collaborator port.
                | _statement_parser - Individual statement parser port.
            :methods:
                | __init__ - Initializes parser with cursor and statement parser.
                | parse - Parses tokens into top-level AST instructions.
                | validate_syntax - Validates token sequence without raising.
    '''

    VALID_MESSAGE: ClassVar[str] = 'Syntax valid'

    _cursor: ITokenCursor
    _statement_parser: IStatementParser

    def __init__(
        self,
        *,
        cursor: ITokenCursor,
        statement_parser: IStatementParser,
    ) -> None:
        '''
            Initializes parser with injected cursor and statement parser ports.

            :param cursor: Token cursor collaborator port.
            :param statement_parser: Individual statement parser port.
            :exceptions: None.
        '''
        self._cursor = cursor
        self._statement_parser = statement_parser

    def parse(self, tokens: Sequence[Token]) -> list[AstInstruction]:
        '''
            Parses tokens into top-level AST instructions.

            :param tokens: Sequence of lexical tokens from lexer.
            :return: List of AstInstruction nodes.
            :exceptions:
                | DslSyntaxError: On syntax or grammatical error.
        '''
        stream: ITokenCursor = self._cursor.open(tokens)
        instructions: list[AstInstruction] = []

        while not stream.is_at_end():
            stream.skip_newlines()

            if stream.is_at_end():
                break

            instructions.append(self._statement_parser.parse_statement(stream))

        return instructions

    def validate_syntax(self, tokens: Sequence[Token]) -> tuple[bool, str]:
        '''
            Validates token sequence without raising exceptions.

            :param tokens: Sequence of lexical tokens to validate.
            :return: Tuple of (is_valid, message).
            :exceptions: None.
        '''
        try:
            self.parse(tokens)
            return True, self.VALID_MESSAGE
        except DslError as err:
            return False, str(err)
