# -*- coding: UTF-8 -*-

'''
Module
    tbot_dsl_service.py
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
    Provides TbotDslService orchestrating lexing, parsing, and compiling of missions.
'''

from __future__ import annotations

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token import Token
from botracked.core.service.dsl.tbot_compiler import TbotCompiler
from botracked.core.service.dsl.tbot_lexer import TbotLexer
from botracked.core.service.dsl.tbot_parser import TbotParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotDslService:
    '''
        Defines class TbotDslService with attribute(s) and method(s).
        Application service managing the lifecycle of .track mission scripts.

        It defines:

            :attributes:
                | _lexer - Lexical scanner instance.
                | _parser - Abstract syntax tree parser instance.
                | _compiler - Binary step compiler instance.
            :methods:
                | __init__ - Initializes DSL service with sub-components.
                | validate - Validates source script syntax.
                | compile - Parses and compiles mission source into executable steps.
    '''

    _lexer: TbotLexer
    _parser: TbotParser
    _compiler: TbotCompiler

    def __init__(
        self,
        lexer: TbotLexer | None = None,
        parser: TbotParser | None = None,
        compiler: TbotCompiler | None = None,
    ) -> None:
        '''
            Initializes DSL service with collaborative sub-components.

            :param lexer: Optional TbotLexer instance.
            :param parser: Optional TbotParser instance.
            :param compiler: Optional TbotCompiler instance.
            :exceptions: None.
        '''
        self._lexer = lexer if lexer is not None else TbotLexer()
        self._parser = parser if parser is not None else TbotParser()
        self._compiler = compiler if compiler is not None else TbotCompiler()

    def validate(self, source: str) -> tuple[bool, str]:
        '''
            Validates source script syntax without generating executable code.

            :param source: Raw script text.
            :return: Tuple of (True, 'Valid') or (False, error_message).
            :exceptions: None.
        '''
        try:
            tokens: list[Token] = self._lexer.tokenize(source)
            ast: list[AstInstruction] = self._parser.parse(tokens)
            steps: list[CompiledStep] = self._compiler.compile(ast)

            return True, f'Validation successful: {len(steps)} steps generated.'

        except Exception as err:
            return False, f'Syntax error: {err}'

    def compile(self, source: str) -> list[CompiledStep]:
        '''
            Parses and compiles mission source into executable steps.

            :param source: Raw script text.
            :return: List of CompiledStep instances.
            :exceptions:
                | ValueError: On any parsing or validation failure.
        '''
        tokens: list[Token] = self._lexer.tokenize(source)
        ast: list[AstInstruction] = self._parser.parse(tokens)

        return self._compiler.compile(ast)
