# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Unit tests for TbotDslService.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.service.dsl.compiler.dependencies import CompilerDependencies
from botracked.core.service.dsl.compiler.factory import CompilerFactory
from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.dsl.lexer.factory import LexerFactory
from botracked.core.service.dsl.parser.factory import ParserFactory
from botracked.core.service.dsl.service import TbotDslService
from botracked.infrastructure.codec.crc.dependencies import CrcDependencies
from botracked.infrastructure.codec.crc.factory import CrcFactory
from botracked.infrastructure.codec.dependencies import CodecDependencies
from botracked.infrastructure.codec.factory import CodecFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotDslServiceTest(TestCase):
    '''
        Defines test methods for TbotDslService behavior.
    '''

    _service: TbotDslService

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        codec = CodecFactory.create(
            CodecDependencies(
                crc_calculator=CrcFactory.create(
                    CrcDependencies(polynomial=0x07)
                ).calculator
            )
        ).codec
        self._service = TbotDslService(
            lexer=LexerFactory.create().lexer,
            parser=ParserFactory.create().parser,
            compiler=CompilerFactory.create(
                CompilerDependencies(codec=codec, default_speed=180)
            ).compiler,
        )

    def test_protocol_and_compile(self) -> None:
        '''
            Verifies ITbotDslService conformance, linear compile, and REPEAT loop.

            :exceptions: None.
        '''
        self.assertIsInstance(self._service, ITbotDslService)
        linear_steps = self._service.compile('SPEED 200\nFORWARD 1.5\nSTOP\n')
        self.assertEqual(len(linear_steps), 3)
        loop_steps = self._service.compile('REPEAT 3\nFORWARD 1.0\nEND\n')
        self.assertEqual(len(loop_steps), 3)

    def test_validate_success_and_failure(self) -> None:
        '''
            Verifies syntax validation success and error reporting.

            :exceptions: None.
        '''
        is_valid, msg = self._service.validate('SPEED 180\nSTOP\n')
        self.assertTrue(is_valid)
        self.assertIn('Validation successful', msg)

        bad_valid, bad_msg = self._service.validate('REPEAT 2\nFORWARD 1.0\n')
        self.assertFalse(bad_valid)
        self.assertIn('Syntax error', bad_msg)

    def test_estimate_duration_and_count_tokens(self) -> None:
        '''
            Verifies total duration estimation and lexical token count.

            :exceptions: None.
        '''
        dur = self._service.estimate_duration('FORWARD 2.0\nWAIT 1.5\nSTOP\n')
        self.assertAlmostEqual(dur, 3.5)
        self.assertEqual(self._service.count_tokens('SPEED 150\n'), 4)


if __name__ == '__main__':
    main()
