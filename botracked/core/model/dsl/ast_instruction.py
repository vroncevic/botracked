# -*- coding: UTF-8 -*-

'''
Module
    ast_instruction.py
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
    Defines AstInstruction node representing parsed mission statements.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class AstInstruction:
    '''
        Defines immutable AST node for an executable mission statement.
        Represents parsed mission syntax tree elements with line tracking.

        It defines:

            :attributes:
                | token_type - Token type of this instruction.
                | param1 - First numerical argument or None.
                | param2 - Second numerical argument or None.
                | line_number - 1-based source line number for diagnostics.
                | children - Nested child instructions for block statements.
            :methods:
                | is_block - Checks if this node represents a block statement.
                | has_children - Checks if instruction contains child elements.
                | summary - Returns a concise diagnostic string representation.
    '''

    token_type: TokenType
    param1: float | int | None = None
    param2: float | int | None = None
    line_number: int = 1
    children: tuple[AstInstruction, ...] = field(default_factory=tuple)

    @property
    def is_block(self) -> bool:
        '''
            Checks if this node represents a block with nested statements.

            :return: True if block statement (e.g. REPEAT), False otherwise.
            :exceptions: None.
        '''
        return self.token_type == TokenType.REPEAT

    @property
    def has_children(self) -> bool:
        '''
            Checks whether this instruction contains child instructions.

            :return: True if children tuple is not empty, False otherwise.
            :exceptions: None.
        '''
        return len(self.children) > 0

    @property
    def summary(self) -> str:
        '''
            Returns a concise representation of the instruction.

            :return: String summary of instruction.
            :exceptions: None.
        '''
        params: list[str] = []

        if self.param1 is not None:
            params.append(str(self.param1))

        if self.param2 is not None:
            params.append(str(self.param2))

        args: str = f" ({', '.join(params)})" if params else ''

        return f'{self.token_type.name}{args} [L{self.line_number}]'
