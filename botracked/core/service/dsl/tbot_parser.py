# -*- coding: UTF-8 -*-

'''
Module
    tbot_parser.py
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
    Provides TbotParser parsing tokens into validated AstInstruction AST nodes.
'''

from __future__ import annotations

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotParser:
    '''
        Defines class TbotParser with attribute(s) and method(s).
        Recursive descent parser constructing AST from .track token streams.

        It defines:

            :attributes:
                | _tokens - Token list being processed.
                | _pos - Current index position within token stream.
            :methods:
                | __init__ - Initializes parser state.
                | parse - Parses tokens into top-level AST instructions.
                | validate_syntax - Validates token sequence without exceptions.
                | _current - Returns the token at current position.
                | _advance - Advances parser position and returns token.
                | _is_at_end - Checks if parser reached EOF.
                | _skip_newlines - Skips newline tokens in stream.
                | _parse_statement - Parses a single AST instruction statement.
    '''

    _tokens: list[Token]
    _pos: int

    def __init__(self) -> None:
        '''
            Initializes parser state.

            :exceptions: None.
        '''
        self._tokens = []
        self._pos = 0

    def parse(self, tokens: list[Token]) -> list[AstInstruction]:
        '''
            Parses tokens into top-level AST instructions.

            :param tokens: List of tokens from lexer.
            :return: List of AstInstruction nodes.
            :exceptions:
                | ValueError: On syntax or grammatical error.
        '''
        self._tokens = tokens
        self._pos = 0
        instructions: list[AstInstruction] = []

        while not self._is_at_end():
            self._skip_newlines()

            if self._is_at_end():
                break

            stmt: AstInstruction | None = self._parse_statement()

            if stmt is not None:
                instructions.append(stmt)

        return instructions

    def validate_syntax(self, tokens: list[Token]) -> tuple[bool, str]:
        '''
            Validates token sequence without throwing exceptions.

            :param tokens: List of lexical tokens to validate.
            :return: Tuple of (is_valid, error_message).
            :exceptions: None.
        '''
        try:
            self.parse(tokens)

            return True, 'Syntax valid'

        except ValueError as err:
            return False, str(err)

    def _current(self) -> Token:
        '''
            Returns the token at current position.

            :return: Current Token instance.
            :exceptions: None.
        '''
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]

        return self._tokens[-1]

    def _advance(self) -> Token:
        '''
            Advances parser position and returns current token.

            :return: Current Token instance before incrementing.
            :exceptions: None.
        '''
        token: Token = self._current()

        if not self._is_at_end():
            self._pos += 1

        return token

    def _is_at_end(self) -> bool:
        '''
            Checks if parser reached end-of-file.

            :return: True if EOF token reached, False otherwise.
            :exceptions: None.
        '''
        return self._current().token_type == TokenType.EOF

    def _skip_newlines(self) -> None:
        '''
            Skips consecutive newline tokens in stream.

            :exceptions: None.
        '''
        while not self._is_at_end() and self._current().token_type == TokenType.NEWLINE:
            self._advance()

    def _parse_speed_statement(self, line: int) -> AstInstruction:
        '''
            Parses SPEED parameter statement.

            :param line: Source line number.
            :return: AstInstruction for SPEED.
            :exceptions:
                | ValueError: If speed is missing or not in range 0..255.
        '''
        speed_tok: Token = self._current()

        if speed_tok.token_type != TokenType.NUMBER or not isinstance(speed_tok.value, (int, float)):
            raise ValueError(f'Line {line}: SPEED expects integer value (0..255)')

        self._advance()
        val: int = int(speed_tok.value)

        if not 0 <= val <= 255:
            raise ValueError(f'Line {line}: SPEED value {val} out of range (0..255)')

        return AstInstruction(TokenType.SPEED, param1=val, line_number=line)

    def _parse_motion_statement(self, tok: Token, line: int) -> AstInstruction:
        '''
            Parses motion statement with optional duration and speed override.

            :param tok: Motion token (e.g. FORWARD, BACKWARD).
            :param line: Source line number.
            :return: AstInstruction for motion command.
            :exceptions:
                | ValueError: If speed override is outside range 0..255.
        '''
        dur: float | None = None
        spd: int | None = None

        if self._current().token_type == TokenType.NUMBER:
            tok_dur = self._advance()

            if isinstance(tok_dur.value, (int, float, str)):
                dur = float(tok_dur.value)

            if self._current().token_type == TokenType.NUMBER:
                tok_spd = self._advance()

                if isinstance(tok_spd.value, (int, float, str)):
                    spd_val: int = int(tok_spd.value)

                    if not 0 <= spd_val <= 255:
                        raise ValueError(f'Line {line}: speed override {spd_val} out of range (0..255)')

                    spd = spd_val

        return AstInstruction(tok.token_type, param1=dur, param2=spd, line_number=line)

    def _parse_wait_statement(self, line: int) -> AstInstruction:
        '''
            Parses WAIT duration statement.

            :param line: Source line number.
            :return: AstInstruction for WAIT command.
            :exceptions:
                | ValueError: If duration is missing or non-numerical.
        '''
        dur_tok: Token = self._current()

        if dur_tok.token_type != TokenType.NUMBER or not isinstance(dur_tok.value, (int, float)):
            raise ValueError(f'Line {line}: WAIT expects duration in seconds')

        self._advance()

        return AstInstruction(TokenType.WAIT, param1=float(dur_tok.value), line_number=line)

    def _parse_repeat_statement(self, line: int) -> AstInstruction:
        '''
            Parses REPEAT loop block statement.

            :param line: Source line number.
            :return: AstInstruction for REPEAT block with children.
            :exceptions:
                | ValueError: If count is missing or block is unclosed.
        '''
        count_tok: Token = self._current()

        if count_tok.token_type != TokenType.NUMBER or not isinstance(count_tok.value, (int, float)):
            raise ValueError(f'Line {line}: REPEAT expects loop count integer')

        self._advance()
        count: int = int(count_tok.value)

        if self._current().token_type == TokenType.COLON:
            self._advance()

        children: list[AstInstruction] = []

        while not self._is_at_end():
            self._skip_newlines()

            if self._is_at_end() or self._current().token_type == TokenType.END:
                break

            child: AstInstruction | None = self._parse_statement()

            if child is not None:
                children.append(child)

        if self._current().token_type != TokenType.END:
            raise ValueError(f'Line {line}: REPEAT block unclosed, missing END')

        self._advance()

        return AstInstruction(
            TokenType.REPEAT, param1=count, line_number=line, children=tuple(children)
        )

    def _parse_statement(self) -> AstInstruction | None:
        '''
            Parses a single AST instruction statement.

            :return: Parsed AstInstruction or None if empty line.
            :exceptions:
                | ValueError: On unrecognized or malformed syntax.
        '''
        tok: Token = self._advance()
        line: int = tok.line

        if tok.token_type == TokenType.SPEED:
            return self._parse_speed_statement(line)

        if tok.token_type in (
            TokenType.FORWARD, TokenType.BACKWARD, TokenType.TURN_LEFT,
            TokenType.TURN_RIGHT, TokenType.SPIN_LEFT, TokenType.SPIN_RIGHT
        ):
            return self._parse_motion_statement(tok, line)

        if tok.token_type == TokenType.WAIT:
            return self._parse_wait_statement(line)

        if tok.token_type in (TokenType.STOP, TokenType.PING, TokenType.CLEAR_ERRORS):
            return AstInstruction(tok.token_type, line_number=line)

        if tok.token_type == TokenType.REPEAT:
            return self._parse_repeat_statement(line)

        if tok.token_type == TokenType.NEWLINE:
            return None

        raise ValueError(f'Line {line}: Unexpected token {tok.lexeme!r}')
