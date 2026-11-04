# -*- coding: UTF-8 -*-

'''
Module
    cursor_test.py
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
    Unit tests for TokenCursor.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.dsl.parser.cursor.cursor import TokenCursor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TokenCursorTest(TestCase):
    '''
        Defines test methods for TokenCursor behavior.
    '''

    def test_empty_and_eof_tokens(self) -> None:
        '''
            Verifies sentinel EOF behavior on empty and exhausted streams.

            :exceptions: None.
        '''
        cursor = TokenCursor(())
        self.assertTrue(cursor.is_at_end())
        self.assertEqual(cursor.current().token_type, TokenType.EOF)
        eof_cursor = cursor.open([Token(TokenType.EOF, '', 1, 1)])
        self.assertTrue(eof_cursor.is_at_end())

    def test_advance_and_reload(self) -> None:
        '''
            Verifies advancing through tokens and isolated open cursor.

            :exceptions: None.
        '''
        tok1 = Token(TokenType.SPEED, 'SPEED', 1, 1)
        tok2 = Token(TokenType.NUMBER, '100', 1, 7)
        tok_eof = Token(TokenType.EOF, '', 2, 1)
        cursor = TokenCursor([tok1, tok2, tok_eof])
        self.assertEqual(cursor.advance(), tok1)
        self.assertEqual(cursor.advance(), tok2)
        self.assertTrue(cursor.is_at_end())
        self.assertEqual(cursor.advance(), tok_eof)

        short_cursor = cursor.open([tok1])
        short_cursor.advance()
        self.assertEqual(short_cursor.current(), tok1)

    def test_skip_newlines(self) -> None:
        '''
            Verifies skipping consecutive newline tokens.

            :exceptions: None.
        '''
        tok1 = Token(TokenType.SPEED, 'SPEED', 1, 1)
        nl1 = Token(TokenType.NEWLINE, '\n', 1, 10)
        nl2 = Token(TokenType.NEWLINE, '\n', 2, 1)
        tok3 = Token(TokenType.STOP, 'STOP', 3, 1)
        cursor = TokenCursor([tok1, nl1, nl2, tok3])
        cursor.advance()
        cursor.skip_newlines()
        self.assertEqual(cursor.current(), tok3)


if __name__ == '__main__':
    main()
