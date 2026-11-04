# -*- coding: UTF-8 -*-

'''
Module
    number_test.py
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
    Unit tests for NumberScanner.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.dsl.lexer.number.number import NumberScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NumberScannerTestCase(TestCase):
    '''
        Defines test methods for NumberScanner behavior.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_is_number_start - Verifies number detection predicates.
                | test_scan_integer - Verifies scanning integer literal.
                | test_scan_float - Verifies scanning floating point literal.
                | test_scan_multiple_dots - Verifies stopping on second dot.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.scanner = NumberScanner()

    def test_is_number_start(self) -> None:
        '''
            Verifies number detection predicates.

            :exceptions: None.
        '''
        self.assertTrue(self.scanner.is_number_start('5', 1, '500'))
        self.assertTrue(self.scanner.is_number_start('.', 1, '.5'))
        self.assertFalse(self.scanner.is_number_start('.', 2, '..'))
        self.assertFalse(self.scanner.is_number_start('a', 1, 'abc'))

    def test_scan_integer(self) -> None:
        '''
            Verifies scanning integer literal.

            :exceptions: None.
        '''
        tok, col = self.scanner.scan('SPEED 250', 7, 1)
        self.assertEqual(tok.token_type, TokenType.NUMBER)
        self.assertEqual(tok.value, '250')
        self.assertEqual(tok.column, 7)
        self.assertEqual(col, 10)

    def test_scan_float(self) -> None:
        '''
            Verifies scanning floating point literal.

            :exceptions: None.
        '''
        tok, col = self.scanner.scan('WAIT 1.75', 6, 2)
        self.assertEqual(tok.token_type, TokenType.NUMBER)
        self.assertEqual(tok.value, '1.75')
        self.assertEqual(col, 10)

    def test_scan_multiple_dots(self) -> None:
        '''
            Verifies stopping on second dot.

            :exceptions: None.
        '''
        tok, col = self.scanner.scan('1.2.3', 1, 1)
        self.assertEqual(tok.value, '1.2')
        self.assertEqual(col, 4)


if __name__ == '__main__':
    main()
