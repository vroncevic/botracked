# -*- coding: UTF-8 -*-

'''
Module
    dsl_compiler_test.py
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
    Unit tests for DSL Lexer, Parser, and Compiler pipeline.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from botracked.core.service.dsl.tbot_compiler import TbotCompiler
from botracked.core.service.dsl.tbot_dsl_service import TbotDslService
from botracked.core.service.dsl.tbot_lexer import TbotLexer
from botracked.core.service.dsl.tbot_parser import TbotParser
from botracked.infrastructure.communication.binary_codec import (
    BinaryCodec,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslCompiler(TestCase):
    '''
    Tests full DSL compilation workflow from .track text into compiled binary frames.
    '''

    _service: TbotDslService

    def setUp(self) -> None:
        self._service = TbotDslService(
            lexer=TbotLexer(),
            parser=TbotParser(),
            compiler=TbotCompiler(codec=BinaryCodec()),
        )

    def test_compile_simple_script(self) -> None:
        '''
        Verifies simple linear script compilation.
        '''
        script = '''
        # Simple test
        SPEED 200
        FORWARD 500
        STOP
        '''
        is_valid, _ = self._service.validate(script)
        self.assertTrue(is_valid)
        steps = self._service.compile(script)
        # SPEED + FORWARD + STOP after duration + explicit STOP
        self.assertGreaterEqual(len(steps), 3)

    def test_compile_repeat_loop(self) -> None:
        '''
        Verifies repeat loop expansion.
        '''
        script = '''
        REPEAT 3
            FORWARD 200
        END
        '''
        is_valid, _ = self._service.validate(script)
        self.assertTrue(is_valid)
        steps = self._service.compile(script)
        self.assertEqual(len(steps), 3)

    def test_syntax_error_reporting(self) -> None:
        '''
        Verifies parser catches invalid or unclosed blocks.
        '''
        script = 'REPEAT 3\nFORWARD 100'  # missing END
        is_valid, error_msg = self._service.validate(script)
        self.assertFalse(is_valid)
        self.assertIn('Syntax error', error_msg)


if __name__ == '__main__':
    main()
