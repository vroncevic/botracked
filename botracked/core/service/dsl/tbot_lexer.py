# -*- coding: UTF-8 -*-

'''
Module
    tbot_lexer.py
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
    Provides TbotLexer scanning .track mission language statements into tokens.
'''

from __future__ import annotations

from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotLexer:
    '''
        Defines class TbotLexer with attribute(s) and method(s).
        Lexical scanner for tracked robot mission scripting language.

        It defines:

            :attributes:
                | _KEYWORDS - Mapping from keyword string literals to TokenType.
            :methods:
                | tokenize - Scans source code text and returns list of tokens.
                | count_tokens - Scans source code and returns token count.
    '''

    _KEYWORDS: dict[str, TokenType] = {
        'SPEED': TokenType.SPEED,
        'FORWARD': TokenType.FORWARD,
        'BACKWARD': TokenType.BACKWARD,
        'TURN_LEFT': TokenType.TURN_LEFT,
        'TURN_RIGHT': TokenType.TURN_RIGHT,
        'SPIN_LEFT': TokenType.SPIN_LEFT,
        'SPIN_RIGHT': TokenType.SPIN_RIGHT,
        'WAIT': TokenType.WAIT,
        'STOP': TokenType.STOP,
        'PING': TokenType.PING,
        'CLEAR_ERRORS': TokenType.CLEAR_ERRORS,
        'REPEAT': TokenType.REPEAT,
        'END': TokenType.END,
    }

    def _scan_number(self, line: str, col: int, line_idx: int) -> tuple[Token, int]:
        '''
            Scans a numerical literal from the line.

            :param line: Source text line.
            :type line: str

            :param col: Starting column index (1-based).
            :type col: int

            :param line_idx: Line number (1-based).
            :type line_idx: int

            :return: Tuple of generated Token and updated column index.
            :rtype: tuple[Token, int]

            :exceptions: None.
        '''
        start_col: int = col
        num_str: str = ''
        has_dot: bool = False
        length: int = len(line)
        while col <= length and (line[col - 1].isdigit() or line[col - 1] == '.'):
            if line[col - 1] == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += line[col - 1]
            col += 1
        val: float | int = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, num_str, val, line_idx, start_col), col

    def _scan_identifier(self, line: str, col: int, line_idx: int) -> tuple[Token, int]:
        '''
            Scans an identifier or reserved keyword from the line.

            :param line: Source text line.
            :type line: str

            :param col: Starting column index (1-based).
            :type col: int

            :param line_idx: Line number (1-based).
            :type line_idx: int

            :return: Tuple of generated Token and updated column index.
            :rtype: tuple[Token, int]

            :exceptions: None.
        '''
        start_col: int = col
        ident: str = ''
        length: int = len(line)
        while col <= length and (line[col - 1].isalnum() or line[col - 1] == '_'):
            ident += line[col - 1]
            col += 1
        tok_type: TokenType = self._KEYWORDS.get(ident.upper(), TokenType.IDENTIFIER)
        return Token(tok_type, ident, ident, line_idx, start_col), col

    def _tokenize_line(self, line: str, line_idx: int, tokens: list[Token]) -> None:
        '''
            Tokenizes a single source line and appends to token list.

            :param line: Source text line.
            :type line: str

            :param line_idx: Line index.
            :type line_idx: int

            :param tokens: Token accumulation list.
            :type tokens: list[Token]

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        col: int = 1
        length: int = len(line)
        while col <= length:
            ch: str = line[col - 1]
            if ch in (' ', '\t', '\r'):
                col += 1
            elif ch == '#':
                break
            elif ch == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', None, line_idx, col))
                col += 1
            elif ch == ':':
                tokens.append(Token(TokenType.COLON, ':', None, line_idx, col))
                col += 1
            elif ch.isdigit() or (ch == '.' and col < length and line[col].isdigit()):
                tok, col = self._scan_number(line, col, line_idx)
                tokens.append(tok)
            elif ch.isalpha() or ch == '_':
                tok, col = self._scan_identifier(line, col, line_idx)
                tokens.append(tok)
            else:
                col += 1

    def tokenize(self, source: str) -> list[Token]:
        '''
            Scans source code text and returns list of tokens.

            :param source: Input mission script text.
            :type source: str

            :return: List of Token objects.
            :rtype: list[Token]

            :exceptions: None.
        '''
        tokens: list[Token] = []
        lines: list[str] = source.splitlines(keepends=True)
        for line_idx, line in enumerate(lines, start=1):
            self._tokenize_line(line, line_idx, tokens)
        tokens.append(Token(TokenType.EOF, '', None, len(lines) + 1, 1))
        return tokens

    def count_tokens(self, source: str) -> int:
        '''
            Scans source code and returns total number of lexical tokens.

            :param source: Raw text content of .track script.
            :type source: str

            :return: Integer count of tokens including EOF.
            :rtype: int

            :exceptions: None.
        '''
        return len(self.tokenize(source))
