# -*- coding: UTF-8 -*-

'''
Module
    statement.py
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
    Defines stateless StatementParser parsing individual .track statements.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token import Token
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.service.dsl.parser.cursor.icursor import ITokenCursor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatementParser:
    '''
        Defines class StatementParser implementing IStatementParser structurally.
        Stateless grammar parser for individual mission script statement forms.

        It defines:

            :attributes:
                | MIN_SPEED - Minimum valid PWM speed byte.
                | MAX_SPEED - Maximum valid PWM speed byte.
                | MIN_REPEAT_COUNT - Minimum non-negative loop iteration count.
            :methods:
                | parse_speed - Parses SPEED configuration statement.
                | parse_motion - Parses locomotion command statement.
                | parse_wait - Parses WAIT duration statement.
                | parse_repeat - Parses REPEAT block statement with nested children.
                | parse_statement - Parses next statement into AstInstruction.
    '''

    MIN_SPEED: ClassVar[int] = 0
    MAX_SPEED: ClassVar[int] = 255
    MIN_REPEAT_COUNT: ClassVar[int] = 0

    def parse_speed(self, cursor: ITokenCursor, line: int) -> AstInstruction:
        '''
            Parses SPEED configuration statement.

            :param cursor: Active token cursor stream.
            :param line: Source line number.
            :return: AstInstruction node for speed.
            :exceptions:
                | DslSyntaxError: If speed value is missing or out of 0..255 range.
        '''
        speed_tok: Token = cursor.current()

        if speed_tok.token_type != TokenType.NUMBER:
            raise DslSyntaxError(
                f'Line {line}: SPEED expects integer value (0..255)'
            )

        cursor.advance()
        val: int = int(float(speed_tok.value))

        if not self.MIN_SPEED <= val <= self.MAX_SPEED:
            raise DslSyntaxError(
                f'Line {line}: SPEED value {val} out of range (0..255)'
            )

        return AstInstruction(
            token_type=TokenType.SPEED,
            line_number=line,
            parameters=(float(val),),
            children=(),
        )

    def parse_motion(
        self, cursor: ITokenCursor, tok: Token, line: int
    ) -> AstInstruction:
        '''
            Parses locomotion command statement with optional duration and speed.

            :param cursor: Active token cursor stream.
            :param tok: Motion token (e.g. FORWARD, BACKWARD).
            :param line: Source line number.
            :return: AstInstruction node for motion command.
            :exceptions:
                | DslSyntaxError: If speed override is outside range 0..255.
        '''
        params_list: list[float] = []

        if cursor.current().token_type == TokenType.NUMBER:
            tok_dur: Token = cursor.advance()
            params_list.append(float(tok_dur.value))

            if cursor.current().token_type == TokenType.NUMBER:
                tok_spd: Token = cursor.advance()
                spd_val: int = int(float(tok_spd.value))

                if not self.MIN_SPEED <= spd_val <= self.MAX_SPEED:
                    raise DslSyntaxError(
                        f'Line {line}: speed override {spd_val} out of range (0..255)'
                    )

                params_list.append(float(spd_val))

        return AstInstruction(
            token_type=tok.token_type,
            line_number=line,
            parameters=tuple(params_list),
            children=(),
        )

    def parse_wait(self, cursor: ITokenCursor, line: int) -> AstInstruction:
        '''
            Parses WAIT duration statement.

            :param cursor: Active token cursor stream.
            :param line: Source line number.
            :return: AstInstruction node for wait.
            :exceptions:
                | DslSyntaxError: If duration value is missing or non-numerical.
        '''
        dur_tok: Token = cursor.current()

        if dur_tok.token_type != TokenType.NUMBER:
            raise DslSyntaxError(f'Line {line}: WAIT expects duration in seconds')

        cursor.advance()

        return AstInstruction(
            token_type=TokenType.WAIT,
            line_number=line,
            parameters=(float(dur_tok.value),),
            children=(),
        )

    def parse_repeat(self, cursor: ITokenCursor, line: int) -> AstInstruction:
        '''
            Parses REPEAT block statement with nested children.

            :param cursor: Active token cursor stream.
            :param line: Source line number.
            :return: AstInstruction node for repeat block.
            :exceptions:
                | DslSyntaxError: If loop count is missing or block is unclosed.
        '''
        count_tok: Token = cursor.current()

        if count_tok.token_type != TokenType.NUMBER:
            raise DslSyntaxError(f'Line {line}: REPEAT expects loop count integer')

        cursor.advance()
        count: int = int(float(count_tok.value))

        if count < self.MIN_REPEAT_COUNT:
            raise DslSyntaxError(
                f'Line {line}: REPEAT count {count} must be non-negative'
            )

        if cursor.current().token_type == TokenType.COLON:
            cursor.advance()

        children: list[AstInstruction] = []

        while not cursor.is_at_end():
            cursor.skip_newlines()

            if cursor.is_at_end() or cursor.current().token_type == TokenType.END:
                break

            children.append(self.parse_statement(cursor))

        if cursor.current().token_type != TokenType.END:
            raise DslSyntaxError(
                f'Line {line}: REPEAT block unclosed, missing END'
            )

        cursor.advance()

        return AstInstruction(
            token_type=TokenType.REPEAT,
            line_number=line,
            parameters=(float(count),),
            children=tuple(children),
        )

    def parse_statement(self, cursor: ITokenCursor) -> AstInstruction:
        '''
            Parses next statement from cursor into AstInstruction.

            :param cursor: Active token cursor stream.
            :return: Parsed AstInstruction node.
            :exceptions:
                | DslSyntaxError: On unexpected or malformed token.
        '''
        cursor.skip_newlines()
        tok: Token = cursor.advance()
        line: int = tok.line

        match tok.token_type:
            case TokenType.SPEED:
                return self.parse_speed(cursor, line)
            case (
                TokenType.FORWARD
                | TokenType.BACKWARD
                | TokenType.TURN_LEFT
                | TokenType.TURN_RIGHT
                | TokenType.SPIN_LEFT
                | TokenType.SPIN_RIGHT
            ):
                return self.parse_motion(cursor, tok, line)
            case TokenType.WAIT:
                return self.parse_wait(cursor, line)
            case TokenType.STOP | TokenType.PING | TokenType.CLEAR_ERRORS:
                return AstInstruction(
                    token_type=tok.token_type,
                    line_number=line,
                    parameters=(),
                    children=(),
                )
            case TokenType.REPEAT:
                return self.parse_repeat(cursor, line)
            case _:
                raise DslSyntaxError(
                    f'Line {line}: Unexpected token {tok.value!r}'
                )
