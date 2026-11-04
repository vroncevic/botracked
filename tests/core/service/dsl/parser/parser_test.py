# -*- coding: UTF-8 -*-

'''
Module
    parser_test.py
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
    Unit tests for TbotParser.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.dsl.parser.cursor.cursor import TokenCursor
from botracked.core.service.dsl.parser.iparser import ITbotParser
from botracked.core.service.dsl.parser.parser import TbotParser
from botracked.core.service.dsl.parser.statement.statement import StatementParser

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotParserTest(TestCase):
    '''
        Defines test methods for TbotParser behavior.
    '''

    _parser: TbotParser

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        cursor = TokenCursor(())
        self._parser = TbotParser(
            cursor=cursor,
            statement_parser=StatementParser(),
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies ITbotParser protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self._parser, ITbotParser)

    def test_parse_success(self) -> None:
        '''
            Verifies parsing token sequence into AST nodes.

            :exceptions: None.
        '''
        tokens = [
            Token(TokenType.NEWLINE, '\n', 1, 1),
            Token(TokenType.SPEED, 'SPEED', 2, 1),
            Token(TokenType.NUMBER, '180', 2, 7),
            Token(TokenType.NEWLINE, '\n', 2, 10),
            Token(TokenType.STOP, 'STOP', 3, 1),
            Token(TokenType.NEWLINE, '\n', 3, 5),
            Token(TokenType.EOF, '', 4, 1),
        ]
        ast = self._parser.parse(tokens)
        self.assertEqual(len(ast), 2)
        self.assertEqual(ast[0].token_type, TokenType.SPEED)
        self.assertEqual(ast[1].token_type, TokenType.STOP)

    def test_validate_syntax_valid_and_invalid(self) -> None:
        '''
            Verifies syntax validation success and DslError message reporting.

            :exceptions: None.
        '''
        ok, valid_msg = self._parser.validate_syntax([
            Token(TokenType.STOP, 'STOP', 1, 1),
            Token(TokenType.EOF, '', 2, 1),
        ])
        self.assertTrue(ok)
        self.assertEqual(valid_msg, 'Syntax valid')

        bad, err_msg = self._parser.validate_syntax([
            Token(TokenType.SPEED, 'SPEED', 1, 1),
            Token(TokenType.EOF, '', 2, 1),
        ])
        self.assertFalse(bad)
        self.assertIn('Line 1: SPEED expects integer value', err_msg)


if __name__ == '__main__':
    main()
