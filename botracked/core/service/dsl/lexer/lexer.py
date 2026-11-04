# -*- coding: UTF-8 -*-

'''
Module
    lexer.py
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
    Defines TbotLexer scanning mission script text into lexical Token streams.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.service.dsl.lexer.identifier.iidentifier import IIdentifierScanner
from botracked.core.service.dsl.lexer.number.inumber import INumberScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotLexer:
    '''
        Defines class TbotLexer implementing ITbotLexer structurally.
        Lexical scanner orchestrating numeric and identifier token extraction.

        It defines:

            :attributes:
                | START_INDEX - Initial 1-based line and column index.
                | SPACE_CHAR - Horizontal space character delimiter.
                | TAB_CHAR - Horizontal tab character delimiter.
                | CR_CHAR - Carriage return character delimiter.
                | COMMENT_CHAR - Line comment prefix character.
                | NEWLINE_CHAR - Line feed character token value.
                | COLON_CHAR - Block header colon character token value.
                | _number_scanner - Scanner port for numeric literals.
                | _identifier_scanner - Scanner port for keywords and identifiers.
            :methods:
                | __init__ - Initializes lexer with scanner ports.
                | tokenize_line - Scans tokens for a single script line.
                | tokenize - Scans source code text and returns list of tokens.
                | count_tokens - Scans source code and returns token count.
    '''

    START_INDEX: ClassVar[int] = 1
    SPACE_CHAR: ClassVar[str] = ' '
    TAB_CHAR: ClassVar[str] = '\t'
    CR_CHAR: ClassVar[str] = '\r'
    COMMENT_CHAR: ClassVar[str] = '#'
    NEWLINE_CHAR: ClassVar[str] = '\n'
    COLON_CHAR: ClassVar[str] = ':'

    _number_scanner: INumberScanner
    _identifier_scanner: IIdentifierScanner

    def __init__(
        self,
        *,
        number_scanner: INumberScanner,
        identifier_scanner: IIdentifierScanner,
    ) -> None:
        '''
            Initializes lexer with scanner ports.

            :param number_scanner: Scanner port for numeric literals.
            :param identifier_scanner: Scanner port for keywords and identifiers.
            :exceptions: None.
        '''
        self._number_scanner = number_scanner
        self._identifier_scanner = identifier_scanner

    def tokenize_line(
        self, line: str, line_idx: int, tokens: list[Token]
    ) -> None:
        '''
            Scans tokens for a single script line and appends to token list.

            :param line: Source text line.
            :param line_idx: Line index (1-based).
            :param tokens: Token accumulation list.
            :exceptions:
                | DslSyntaxError: If an unrecognized character is encountered.
        '''
        col: int = self.START_INDEX
        length: int = len(line)

        while col <= length:
            ch: str = line[col - 1]

            match ch:
                case self.SPACE_CHAR | self.TAB_CHAR | self.CR_CHAR:
                    col += 1
                case self.COMMENT_CHAR:
                    break
                case self.NEWLINE_CHAR:
                    tokens.append(
                        Token(TokenType.NEWLINE, self.NEWLINE_CHAR, line_idx, col)
                    )
                    col += 1
                case self.COLON_CHAR:
                    tokens.append(
                        Token(TokenType.COLON, self.COLON_CHAR, line_idx, col)
                    )
                    col += 1
                case _ if self._number_scanner.is_number_start(ch, col, line):
                    tok, col = self._number_scanner.scan(line, col, line_idx)
                    tokens.append(tok)
                case _ if self._identifier_scanner.is_identifier_start(ch):
                    tok, col = self._identifier_scanner.scan(line, col, line_idx)
                    tokens.append(tok)
                case _:
                    raise DslSyntaxError(
                        f'Line {line_idx}, column {col}: Unexpected character {ch!r}'
                    )

    def tokenize(self, source: str) -> list[Token]:
        '''
            Scans source code text and returns list of tokens.

            :param source: Input mission script text.
            :return: List of Token objects including EOF.
            :exceptions:
                | DslSyntaxError: If an unrecognized character is encountered.
        '''
        tokens: list[Token] = []
        lines: list[str] = source.splitlines(keepends=True)

        for line_idx, line in enumerate(lines, start=self.START_INDEX):
            self.tokenize_line(line, line_idx, tokens)

        last_line: int = len(lines) + self.START_INDEX
        tokens.append(Token(TokenType.EOF, '', last_line, self.START_INDEX))
        return tokens

    def count_tokens(self, source: str) -> int:
        '''
            Scans source code and returns token count.

            :param source: Input mission script text.
            :return: Total number of tokens produced.
            :exceptions:
                | DslSyntaxError: If an unrecognized character is encountered.
        '''
        return len(self.tokenize(source))
