# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Defines TbotDslService orchestrating lexing, parsing, and compiling of missions.
'''

from __future__ import annotations

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.exceptions.dsl_error import DslError
from botracked.core.service.dsl.compiler.icompiler import ITbotCompiler
from botracked.core.service.dsl.lexer.ilexer import ITbotLexer
from botracked.core.service.dsl.parser.iparser import ITbotParser

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotDslService:
    '''
        Defines class TbotDslService implementing ITbotDslService structurally.
        Application service coordinating lexer, parser, and compiler ports.

        It defines:

            :attributes:
                | _lexer - Lexical scanner collaborator port.
                | _parser - Token parser collaborator port.
                | _compiler - Binary step compiler collaborator port.
            :methods:
                | __init__ - Initializes DSL service with collaborator ports.
                | compile - Parses and compiles mission source into executable steps.
                | validate - Validates source script syntax without raising.
                | estimate_duration - Estimates execution duration in seconds.
                | count_tokens - Counts lexical tokens in script text.
    '''

    _lexer: ITbotLexer
    _parser: ITbotParser
    _compiler: ITbotCompiler

    def __init__(
        self,
        *,
        lexer: ITbotLexer,
        parser: ITbotParser,
        compiler: ITbotCompiler,
    ) -> None:
        '''
            Initializes DSL service with collaborator ports.

            :param lexer: Lexical scanner collaborator port.
            :param parser: Token parser collaborator port.
            :param compiler: Binary step compiler collaborator port.
            :exceptions: None.
        '''
        self._lexer = lexer
        self._parser = parser
        self._compiler = compiler

    def compile(self, source: str) -> list[CompiledStep]:
        '''
            Parses and compiles mission source into executable steps.

            :param source: Raw script text.
            :return: List of CompiledStep instances.
            :exceptions:
                | DslSyntaxError: On parsing or syntax error.
        '''
        tokens = self._lexer.tokenize(source)
        ast = self._parser.parse(tokens)
        return self._compiler.compile(ast)

    def validate(self, source: str) -> tuple[bool, str]:
        '''
            Validates source script syntax without raising exceptions.

            :param source: Raw script text.
            :return: Tuple of (is_valid, report_message).
            :exceptions: None.
        '''
        try:
            steps: list[CompiledStep] = self.compile(source)
            return True, f'Validation successful: {len(steps)} steps generated.'
        except DslError as err:
            return False, f'Syntax error: {err}'

    def estimate_duration(self, source: str) -> float:
        '''
            Estimates execution duration in seconds.

            :param source: Raw script text.
            :return: Total estimated duration in seconds.
            :exceptions:
                | DslSyntaxError: On parsing or syntax error.
        '''
        tokens = self._lexer.tokenize(source)
        ast = self._parser.parse(tokens)
        return self._compiler.estimate_duration(ast)

    def count_tokens(self, source: str) -> int:
        '''
            Counts lexical tokens in script text.

            :param source: Raw script text.
            :return: Integer token count.
            :exceptions: None.
        '''
        return self._lexer.count_tokens(source)
