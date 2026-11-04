# -*- coding: UTF-8 -*-

'''
Module
    lexer_test.py
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
    Unit tests for TbotLexer.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.service.dsl.lexer.identifier.identifier import IdentifierScanner
from botracked.core.service.dsl.lexer.ilexer import ITbotLexer
from botracked.core.service.dsl.lexer.lexer import TbotLexer
from botracked.core.service.dsl.lexer.number.number import NumberScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotLexerTest(TestCase):
    '''
        Defines test methods for TbotLexer behavior.
    '''

    _lexer: TbotLexer

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self._lexer = TbotLexer(
            number_scanner=NumberScanner(),
            identifier_scanner=IdentifierScanner(),
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies ITbotLexer protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self._lexer, ITbotLexer)

    def test_tokenize_script(self) -> None:
        '''
            Verifies scanning complete mission script.

            :exceptions: None.
        '''
        script = 'SPEED 150\nFORWARD 2.5: \nSTOP\n'
        tokens = self._lexer.tokenize(script)
        types = [tok.token_type for tok in tokens]
        self.assertIn(TokenType.SPEED, types)
        self.assertIn(TokenType.NUMBER, types)
        self.assertIn(TokenType.COLON, types)
        self.assertIn(TokenType.STOP, types)
        self.assertEqual(types[-1], TokenType.EOF)

    def test_count_and_comments(self) -> None:
        '''
            Verifies token counting, comment stripping, and invalid character error.

            :exceptions: None.
        '''
        self.assertEqual(self._lexer.count_tokens('STOP\n'), 3)
        tokens = self._lexer.tokenize('STOP # comment\nSTOP\n')
        stop_tokens = [tok for tok in tokens if tok.token_type == TokenType.STOP]
        self.assertEqual(len(stop_tokens), 2)
        with self.assertRaises(DslSyntaxError):
            self._lexer.tokenize('$ STOP\n')


if __name__ == '__main__':
    main()
