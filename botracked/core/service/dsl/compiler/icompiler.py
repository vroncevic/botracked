# -*- coding: UTF-8 -*-

'''
Module
    icompiler.py
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
    Defines ITbotCompiler structural protocol for compiling AST instructions.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITbotCompiler(Protocol):
    '''
        Defines structural protocol ITbotCompiler for AST compilation.

        It defines:

            :methods:
                | compile - Compiles AST instruction sequence into binary steps.
                | estimate_duration - Estimates total execution duration in seconds.
    '''

    def compile(self, ast: Sequence[AstInstruction]) -> list[CompiledStep]:
        '''
            Compiles AST instruction sequence into binary steps.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Ordered list of CompiledStep instances.
        '''

    def estimate_duration(self, ast: Sequence[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds for AST instructions.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Estimated execution time in seconds.
        '''
