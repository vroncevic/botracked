# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Defines TbotCompiler orchestrating stateless AST compilation and duration.
'''

from __future__ import annotations

from collections.abc import Sequence

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.dsl.compiler.estimator.iestimator import IDurationEstimator
from botracked.core.service.dsl.compiler.node.inode import INodeCompiler
from botracked.core.service.dsl.compiler.node.state import SpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotCompiler:
    '''
        Defines class TbotCompiler implementing ITbotCompiler structurally.
        Compiles mission script AST instructions into timed binary frame sequences.

        It defines:

            :attributes:
                | _node_compiler - Stateless recursive AST node compiler port.
                | _estimator - AST execution duration estimator port.
            :methods:
                | __init__ - Initializes compiler with node compiler and estimator.
                | compile - Compiles AST instruction sequence into binary steps.
                | estimate_duration - Estimates total execution duration in seconds.
    '''

    _node_compiler: INodeCompiler
    _estimator: IDurationEstimator

    def __init__(
        self,
        *,
        node_compiler: INodeCompiler,
        estimator: IDurationEstimator,
    ) -> None:
        '''
            Initializes compiler with node compiler and duration estimator ports.

            :param node_compiler: Recursive AST node compiler port.
            :param estimator: AST duration estimator port.
            :exceptions: None.
        '''
        self._node_compiler = node_compiler
        self._estimator = estimator

    def compile(self, ast: Sequence[AstInstruction]) -> list[CompiledStep]:
        '''
            Compiles AST instruction sequence into binary steps.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Ordered list of CompiledStep instances.
            :exceptions:
                | DslSyntaxError: If an AST node token type is unsupported.
        '''
        state: SpeedState = self._node_compiler.initial_state()
        steps: list[CompiledStep] = []

        for node in ast:
            state = self._node_compiler.compile_node(node, steps, state)

        return steps

    def estimate_duration(self, ast: Sequence[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds directly over AST.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Estimated execution time in seconds.
            :exceptions:
                | DslSyntaxError: If an AST node token type is unsupported.
        '''
        return self._estimator.estimate_duration(ast)
