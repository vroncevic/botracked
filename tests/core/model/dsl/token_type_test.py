# -*- coding: UTF-8 -*-

'''
Module
    token_type_test.py
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
    Unit tests for TokenType enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TokenTypeTest(TestCase):
    '''
        Tests TokenType enumeration members and classifications.
    '''

    def test_members_and_values(self) -> None:
        '''
            Verifies instruction keywords and string values.

            :exceptions: None.
        '''
        self.assertEqual(TokenType.FORWARD, 'FORWARD')
        self.assertEqual(TokenType.BACKWARD, 'BACKWARD')
        self.assertEqual(TokenType.STOP, 'STOP')
        self.assertEqual(TokenType.REPEAT, 'REPEAT')
        self.assertEqual(TokenType.END, 'END')
        self.assertEqual(TokenType.NUMBER, 'NUMBER')

    def test_enumeration_membership(self) -> None:
        '''
            Verifies count and presence of key language tokens.

            :exceptions: None.
        '''
        members = list(TokenType)
        self.assertEqual(len(members), 19)
        self.assertIn(TokenType.SPEED, members)
        self.assertIn(TokenType.WAIT, members)
        self.assertIn(TokenType.EOF, members)


if __name__ == '__main__':
    main()
