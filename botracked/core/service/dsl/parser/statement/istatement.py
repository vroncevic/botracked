# -*- coding: UTF-8 -*-

'''
Module
    istatement.py
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
    Defines IStatementParser structural protocol for individual DSL statements.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.service.dsl.parser.cursor.icursor import ITokenCursor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStatementParser(Protocol):
    '''
        Defines structural protocol IStatementParser for DSL grammar statements.

        It defines:

            :methods:
                | parse_statement - Parses next statement from cursor into AST.
                | parse_repeat - Parses REPEAT block statement with children.
    '''

    def parse_statement(self, cursor: ITokenCursor) -> AstInstruction:
        '''
            Parses next statement from token cursor into AstInstruction.

            :param cursor: Active token cursor stream.
            :return: Parsed AstInstruction node.
        '''

    def parse_repeat(self, cursor: ITokenCursor, line: int) -> AstInstruction:
        '''
            Parses REPEAT block statement with nested children.

            :param cursor: Active token cursor stream.
            :param line: Source line number.
            :return: AstInstruction node for repeat block.
        '''
