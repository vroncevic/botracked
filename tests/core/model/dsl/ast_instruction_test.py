# -*- coding: UTF-8 -*-

'''
Module
    ast_instruction_test.py
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
    Unit tests for AstInstruction AST node model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AstInstructionTest(TestCase):
    '''
        Tests AstInstruction initialization, attributes, immutability, and equality.
    '''

    def test_instantiation_and_fields(self) -> None:
        '''
            Verifies field values upon standard instantiation.

            :exceptions: None.
        '''
        child = AstInstruction(
            token_type=TokenType.FORWARD,
            line_number=2,
            parameters=(100.0, 1.5),
            children=()
        )
        parent = AstInstruction(
            token_type=TokenType.REPEAT,
            line_number=1,
            parameters=(3.0,),
            children=(child,)
        )
        self.assertEqual(parent.token_type, TokenType.REPEAT)
        self.assertEqual(parent.line_number, 1)
        self.assertEqual(parent.parameters, (3.0,))
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].token_type, TokenType.FORWARD)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying frozen dataclass attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        node = AstInstruction(
            token_type=TokenType.STOP,
            line_number=5,
            parameters=(),
            children=()
        )
        with self.assertRaises(FrozenInstanceError):
            node.line_number = 10  # type: ignore[misc]

    def test_equality(self) -> None:
        '''
            Verifies equality and inequality of AstInstruction instances.

            :exceptions: None.
        '''
        node1 = AstInstruction(
            token_type=TokenType.SPEED,
            line_number=1,
            parameters=(150.0,),
            children=()
        )
        node2 = AstInstruction(
            token_type=TokenType.SPEED,
            line_number=1,
            parameters=(150.0,),
            children=()
        )
        node3 = AstInstruction(
            token_type=TokenType.SPEED,
            line_number=2,
            parameters=(200.0,),
            children=()
        )
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)


if __name__ == '__main__':
    main()
