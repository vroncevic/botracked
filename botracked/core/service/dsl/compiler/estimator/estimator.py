# -*- coding: UTF-8 -*-

'''
Module
    estimator.py
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
    Defines AstDurationEstimator calculating script execution times from AST.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AstDurationEstimator:
    '''
        Defines class AstDurationEstimator implementing IDurationEstimator.
        Stateless recursive calculator estimating routine duration directly from AST.

        It defines:

            :attributes:
                | ZERO_DURATION - Instantaneous step duration constant.
                | DEFAULT_WAIT_SEC - Fallback wait duration when parameter omitted.
                | DEFAULT_REPEAT_COUNT - Fallback loop iteration count.
            :methods:
                | estimate_duration - Estimates total duration across AST nodes.
                | estimate_node - Estimates execution duration of single AST node.
    '''

    ZERO_DURATION: ClassVar[float] = 0.0
    DEFAULT_WAIT_SEC: ClassVar[float] = 0.5
    DEFAULT_REPEAT_COUNT: ClassVar[int] = 1

    def estimate_duration(self, ast: Sequence[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds across AST sequence.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Total estimated execution duration in seconds.
            :exceptions:
                | DslSyntaxError: If an AST node token type is unsupported.
        '''
        return sum(self.estimate_node(node) for node in ast)

    def estimate_node(self, node: AstInstruction) -> float:
        '''
            Estimates execution duration in seconds directly from an AST node.

            :param node: AST instruction node to evaluate.
            :return: Estimated execution time in seconds.
            :exceptions:
                | DslSyntaxError: If node token type is unsupported.
        '''
        match node.token_type:
            case (
                TokenType.FORWARD
                | TokenType.BACKWARD
                | TokenType.TURN_LEFT
                | TokenType.TURN_RIGHT
                | TokenType.SPIN_LEFT
                | TokenType.SPIN_RIGHT
            ):
                return (
                    node.parameters[0]
                    if node.parameters
                    else self.ZERO_DURATION
                )
            case TokenType.WAIT:
                return (
                    node.parameters[0]
                    if node.parameters
                    else self.DEFAULT_WAIT_SEC
                )
            case TokenType.REPEAT:
                count: int = (
                    int(node.parameters[0])
                    if node.parameters
                    else self.DEFAULT_REPEAT_COUNT
                )
                return count * sum(
                    self.estimate_node(child) for child in node.children
                )
            case (
                TokenType.SPEED
                | TokenType.STOP
                | TokenType.PING
                | TokenType.CLEAR_ERRORS
            ):
                return self.ZERO_DURATION
            case _:
                raise DslSyntaxError(
                    f'Line {node.line_number}: Unsupported AST node '
                    f'{node.token_type.name}'
                )
