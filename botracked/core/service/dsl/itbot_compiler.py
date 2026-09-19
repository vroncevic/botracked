# -*- coding: UTF-8 -*-

'''
Module
    itbot_compiler.py
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
    Defines ITbotCompiler interface for compiling AST into executable binary steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITbotCompiler(Protocol):
    '''
        Defines protocol ITbotCompiler with method(s).
        Protocol for compiling mission AST instructions into executable binary steps.

        It defines:

            :methods:
                | compile - Compiles AST into ordered sequence of timed commands.
                | estimate_duration - Estimates total execution duration in seconds.
    '''

    def compile(self, ast: list[AstInstruction]) -> list[CompiledStep]:
        '''
            Compiles AST into ordered sequence of timed binary commands.

            :param ast: List of parsed AstInstruction nodes.
            :return: List of CompiledStep instances ready for execution.
        '''

    def estimate_duration(self, ast: list[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds for given AST instructions.

            :param ast: List of parsed AstInstruction nodes.
            :return: Estimated execution time in seconds.
        '''
