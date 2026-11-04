# -*- coding: UTF-8 -*-

'''
Module
    statement_test.py
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
    Unit tests for StatementParser.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.service.dsl.parser.cursor.cursor import TokenCursor
from botracked.core.service.dsl.parser.statement.statement import StatementParser

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatementParserTest(TestCase):
    '''
        Defines test methods for StatementParser behavior.
    '''

    _parser: StatementParser

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self._parser = StatementParser()

    def test_speed_and_wait_parsing(self) -> None:
        '''
            Verifies SPEED and WAIT parsing and DslSyntaxError on invalid input.

            :exceptions: None.
        '''
        cursor = TokenCursor([
            Token(TokenType.SPEED, 'SPEED', 1, 1),
            Token(TokenType.NUMBER, '200', 1, 7),
            Token(TokenType.WAIT, 'WAIT', 2, 1),
            Token(TokenType.NUMBER, '3.5', 2, 6),
            Token(TokenType.EOF, '', 3, 1),
        ])
        speed_node = self._parser.parse_statement(cursor)
        wait_node = self._parser.parse_statement(cursor)
        self.assertEqual(speed_node.parameters, (200.0,))
        self.assertEqual(wait_node.parameters, (3.5,))

        for bad_tokens in (
            [Token(TokenType.SPEED, 'SPEED', 1, 1), Token(TokenType.STOP, 'STOP', 1, 7)],
            [Token(TokenType.SPEED, 'SPEED', 1, 1), Token(TokenType.NUMBER, '300', 1, 7)],
            [Token(TokenType.WAIT, 'WAIT', 1, 1), Token(TokenType.STOP, 'STOP', 1, 6)],
        ):
            bad_cursor = TokenCursor(bad_tokens)
            with self.assertRaises(DslSyntaxError):
                self._parser.parse_statement(bad_cursor)

    def test_motion_and_simple_statements(self) -> None:
        '''
            Verifies locomotion commands, speed overrides, and simple commands.

            :exceptions: None.
        '''
        cursor = TokenCursor([
            Token(TokenType.NEWLINE, '\n', 1, 1),
            Token(TokenType.FORWARD, 'FORWARD', 2, 1),
            Token(TokenType.NUMBER, '1.5', 2, 9),
            Token(TokenType.NUMBER, '220', 2, 13),
            Token(TokenType.STOP, 'STOP', 3, 1),
            Token(TokenType.PING, 'PING', 4, 1),
            Token(TokenType.CLEAR_ERRORS, 'CLEAR_ERRORS', 5, 1),
            Token(TokenType.EOF, '', 6, 1),
        ])
        motion = self._parser.parse_statement(cursor)
        self.assertEqual(motion.parameters, (1.5, 220.0))
        self.assertEqual(
            self._parser.parse_statement(cursor).token_type, TokenType.STOP
        )
        self.assertEqual(
            self._parser.parse_statement(cursor).token_type, TokenType.PING
        )
        self.assertEqual(
            self._parser.parse_statement(cursor).token_type,
            TokenType.CLEAR_ERRORS,
        )

        bad_cursor = TokenCursor([
            Token(TokenType.BACKWARD, 'BACKWARD', 1, 1),
            Token(TokenType.NUMBER, '2.0', 1, 10),
            Token(TokenType.NUMBER, '500', 1, 14),
        ])
        with self.assertRaises(DslSyntaxError):
            self._parser.parse_statement(bad_cursor)

    def test_repeat_and_unexpected_token(self) -> None:
        '''
            Verifies REPEAT block parsing and syntax errors on malformed blocks.

            :exceptions: None.
        '''
        cursor = TokenCursor([
            Token(TokenType.REPEAT, 'REPEAT', 1, 1),
            Token(TokenType.NUMBER, '3', 1, 8),
            Token(TokenType.COLON, ':', 1, 9),
            Token(TokenType.NEWLINE, '\n', 1, 10),
            Token(TokenType.FORWARD, 'FORWARD', 2, 5),
            Token(TokenType.NUMBER, '1.0', 2, 13),
            Token(TokenType.END, 'END', 3, 1),
            Token(TokenType.EOF, '', 4, 1),
        ])
        repeat_node = self._parser.parse_statement(cursor)
        self.assertEqual(repeat_node.token_type, TokenType.REPEAT)
        self.assertEqual(len(repeat_node.children), 1)

        for bad_repeat in (
            [Token(TokenType.REPEAT, 'REPEAT', 1, 1), Token(TokenType.COLON, ':', 1, 8)],
            [Token(TokenType.REPEAT, 'REPEAT', 1, 1), Token(TokenType.NUMBER, '-1', 1, 8)],
            [Token(TokenType.REPEAT, 'REPEAT', 1, 1), Token(TokenType.NUMBER, '2', 1, 8), Token(TokenType.EOF, '', 2, 1)],
            [Token(TokenType.IDENTIFIER, 'FOOBAR', 1, 1)],
        ):
            bad_cursor = TokenCursor(bad_repeat)
            with self.assertRaises(DslSyntaxError):
                self._parser.parse_statement(bad_cursor)


if __name__ == '__main__':
    main()
