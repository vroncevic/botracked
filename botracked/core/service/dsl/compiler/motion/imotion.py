# -*- coding: UTF-8 -*-

'''
Module
    imotion.py
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
    Defines IMotionStepCompiler structural protocol for compiling motion steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.dsl.compiler.node.state import SpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMotionStepCompiler(Protocol):
    '''
        Defines structural protocol IMotionStepCompiler for locomotion compilation.

        It defines:

            :methods:
                | is_motion_token - Checks if token represents locomotion command.
                | compile_motion - Compiles locomotion AST node into step and state.
    '''

    def is_motion_token(self, token_type: TokenType) -> bool:
        '''
            Checks if given token type represents a locomotion command.

            :param token_type: DSL token type to inspect.
            :return: True if token is locomotion command, False otherwise.
        '''

    def compile_motion(
        self, node: AstInstruction, state: SpeedState
    ) -> tuple[CompiledStep, SpeedState]:
        '''
            Compiles locomotion AST node into CompiledStep and next SpeedState.

            :param node: Locomotion AST instruction node.
            :param state: Current per-compilation speed state.
            :return: Tuple of generated CompiledStep and updated SpeedState.
        '''
