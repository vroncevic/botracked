# -*- coding: UTF-8 -*-

'''
Module
    inode.py
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
    Defines INodeCompiler structural protocol for compiling individual AST nodes.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
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
class INodeCompiler(Protocol):
    '''
        Defines structural protocol INodeCompiler for stateless AST compilation.

        It defines:

            :methods:
                | initial_state - Creates baseline SpeedState for compilation run.
                | compile_node - Compiles AST node into steps and returns state.
    '''

    def initial_state(self) -> SpeedState:
        '''
            Creates baseline SpeedState initialized to default speed.

            :return: Initial SpeedState instance.
        '''

    def compile_node(
        self,
        node: AstInstruction,
        steps: list[CompiledStep],
        state: SpeedState,
    ) -> SpeedState:
        '''
            Compiles AST instruction node into steps and returns next SpeedState.

            :param node: AST instruction node to compile.
            :param steps: Accumulator list for generated CompiledStep instances.
            :param state: Current per-compilation speed state.
            :return: Updated SpeedState after compiling node.
        '''
