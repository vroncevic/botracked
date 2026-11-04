# -*- coding: UTF-8 -*-

'''
Module
    iestimator.py
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
    Defines IDurationEstimator structural protocol for AST duration estimation.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.ast_instruction import AstInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDurationEstimator(Protocol):
    '''
        Defines structural protocol IDurationEstimator for AST duration estimation.

        It defines:

            :methods:
                | estimate_duration - Estimates total duration over AST sequence.
                | estimate_node - Estimates duration of a single AST node.
    '''

    def estimate_duration(self, ast: Sequence[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds over AST sequence.

            :param ast: Sequence of parsed AstInstruction nodes.
            :return: Total estimated execution duration in seconds.
        '''

    def estimate_node(self, node: AstInstruction) -> float:
        '''
            Estimates execution duration in seconds directly from an AST node.

            :param node: AST instruction node to evaluate.
            :return: Estimated execution time in seconds.
        '''
