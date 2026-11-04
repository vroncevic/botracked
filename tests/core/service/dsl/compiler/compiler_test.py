# -*- coding: UTF-8 -*-

'''
Module
    compiler_test.py
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
    Unit tests for TbotCompiler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.compiler import TbotCompiler
from botracked.core.service.dsl.compiler.estimator.estimator import AstDurationEstimator
from botracked.core.service.dsl.compiler.icompiler import ITbotCompiler
from botracked.core.service.dsl.compiler.motion.motion import MotionStepCompiler
from botracked.core.service.dsl.compiler.node.node import NodeCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotCompilerTest(TestCase):
    '''
        Defines test methods for TbotCompiler behavior.
    '''

    _compiler: TbotCompiler

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        mock_codec = Mock(spec=IBinaryCodec)
        mock_codec.encode_frame.return_value = b'\xaa\x03\x00\x55'
        motion_compiler = MotionStepCompiler(codec=mock_codec)
        node_compiler = NodeCompiler(
            motion_compiler=motion_compiler,
            codec=mock_codec,
            default_speed=180,
        )
        estimator = AstDurationEstimator()
        self._compiler = TbotCompiler(
            node_compiler=node_compiler,
            estimator=estimator,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies ITbotCompiler protocol conformance.

            :exceptions: None.
        '''
        self.assertIsInstance(self._compiler, ITbotCompiler)

    def test_compile_and_estimate_duration(self) -> None:
        '''
            Verifies compilation and duration estimation.

            :exceptions: None.
        '''
        ast = [
            AstInstruction(TokenType.FORWARD, 1, (2.0,), ()),
            AstInstruction(TokenType.WAIT, 2, (1.5,), ()),
            AstInstruction(TokenType.STOP, 3, (), ()),
        ]
        steps = self._compiler.compile(ast)
        self.assertEqual(len(steps), 3)
        self.assertAlmostEqual(self._compiler.estimate_duration(ast), 3.5)


if __name__ == '__main__':
    main()
