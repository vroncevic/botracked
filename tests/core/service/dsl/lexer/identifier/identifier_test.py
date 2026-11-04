# -*- coding: UTF-8 -*-

'''
Module
    identifier_test.py
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
    Unit tests for IdentifierScanner.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.dsl.lexer.identifier.identifier import IdentifierScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IdentifierScannerTestCase(TestCase):
    '''
        Defines test methods for IdentifierScanner behavior.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_is_identifier_start - Verifies identifier start predicates.
                | test_scan_keywords - Verifies keyword recognition.
                | test_scan_generic_identifier - Verifies non-keyword identifier scanning.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.scanner = IdentifierScanner()

    def test_is_identifier_start(self) -> None:
        '''
            Verifies identifier start predicates.

            :exceptions: None.
        '''
        self.assertTrue(self.scanner.is_identifier_start('a'))
        self.assertTrue(self.scanner.is_identifier_start('Z'))
        self.assertTrue(self.scanner.is_identifier_start('_'))
        self.assertFalse(self.scanner.is_identifier_start('9'))
        self.assertFalse(self.scanner.is_identifier_start(':'))

    def test_scan_keywords(self) -> None:
        '''
            Verifies keyword recognition.

            :exceptions: None.
        '''
        tok, col = self.scanner.scan('FORWARD 100', 1, 1)
        self.assertEqual(tok.token_type, TokenType.FORWARD)
        self.assertEqual(tok.value, 'FORWARD')
        self.assertEqual(col, 8)

        tok_repeat, _ = self.scanner.scan('repeat 5', 1, 1)
        self.assertEqual(tok_repeat.token_type, TokenType.REPEAT)

    def test_scan_generic_identifier(self) -> None:
        '''
            Verifies non-keyword identifier scanning.

            :exceptions: None.
        '''
        tok, col = self.scanner.scan('my_variable 123', 1, 1)
        self.assertEqual(tok.token_type, TokenType.IDENTIFIER)
        self.assertEqual(tok.value, 'my_variable')
        self.assertEqual(col, 12)


if __name__ == '__main__':
    main()
