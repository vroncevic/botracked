# -*- coding: UTF-8 -*-

'''
Module
    token_test.py
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
    Unit tests for Token lexical token model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TokenTest(TestCase):
    '''
        Tests Token initialization, attributes, immutability, and equality.
    '''

    def test_instantiation_and_fields(self) -> None:
        '''
            Verifies field values upon standard instantiation.

            :exceptions: None.
        '''
        token = Token(
            token_type=TokenType.FORWARD,
            value='FORWARD',
            line=5,
            column=0
        )
        self.assertEqual(token.token_type, TokenType.FORWARD)
        self.assertEqual(token.value, 'FORWARD')
        self.assertEqual(token.line, 5)
        self.assertEqual(token.column, 0)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying frozen dataclass attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        token = Token(
            token_type=TokenType.NUMBER,
            value='100',
            line=1,
            column=4
        )
        with self.assertRaises(FrozenInstanceError):
            token.value = '200'  # type: ignore[misc]

    def test_equality(self) -> None:
        '''
            Verifies equality comparison between Token instances.

            :exceptions: None.
        '''
        token1 = Token(TokenType.STOP, 'STOP', 1, 0)
        token2 = Token(TokenType.STOP, 'STOP', 1, 0)
        token3 = Token(TokenType.WAIT, 'WAIT', 1, 0)
        self.assertEqual(token1, token2)
        self.assertNotEqual(token1, token3)


if __name__ == '__main__':
    main()
