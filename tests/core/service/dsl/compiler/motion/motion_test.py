# -*- coding: UTF-8 -*-

'''
Module
    motion_test.py
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
    Unit tests for MotionStepCompiler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.motion.motion import MotionStepCompiler
from botracked.core.service.dsl.compiler.node.state import SpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionStepCompilerTest(TestCase):
    '''
        Tests MotionStepCompiler locomotion step generation.
    '''

    _codec: MagicMock
    _compiler: MotionStepCompiler

    def setUp(self) -> None:
        '''
            Sets up test fixture before each test method.

            :exceptions: None.
        '''
        self._codec = MagicMock(spec=IBinaryCodec)
        self._codec.encode_frame.side_effect = lambda op, payload: b'frame'
        self._compiler = MotionStepCompiler(codec=self._codec)

    def test_compile_motion_with_override(self) -> None:
        '''
            Verifies motion step compilation with speed override parameter.

            :exceptions: None.
        '''
        node = AstInstruction(
            token_type=TokenType.FORWARD,
            line_number=5,
            parameters=(2.0, 220),
            children=(),
        )
        initial_state = SpeedState(current_speed=180, applied_speed=180)
        step, next_state = self._compiler.compile_motion(node, initial_state)

        self.assertIsInstance(step, CompiledStep)
        self.assertEqual(step.duration_sec, 2.0)
        self.assertTrue(step.auto_stop_after)
        self.assertEqual(len(step.frames), 2)
        self.assertIn('speed 220', step.description)
        self.assertEqual(next_state.applied_speed, 220)

    def test_is_motion_token(self) -> None:
        '''
            Verifies is_motion_token identifies locomotion commands correctly.

            :exceptions: None.
        '''
        self.assertTrue(self._compiler.is_motion_token(TokenType.FORWARD))
        self.assertTrue(self._compiler.is_motion_token(TokenType.SPIN_RIGHT))
        self.assertFalse(self._compiler.is_motion_token(TokenType.SPEED))
        self.assertFalse(self._compiler.is_motion_token(TokenType.WAIT))

    def test_compile_motion_without_override(self) -> None:
        '''
            Verifies motion step compilation when applied speed already matches.

            :exceptions: None.
        '''
        node = AstInstruction(
            token_type=TokenType.BACKWARD,
            line_number=10,
            parameters=(),
            children=(),
        )
        initial_state = SpeedState(current_speed=180, applied_speed=180)
        step, next_state = self._compiler.compile_motion(node, initial_state)

        self.assertEqual(step.duration_sec, 0.0)
        self.assertFalse(step.auto_stop_after)
        self.assertEqual(len(step.frames), 1)
        self.assertEqual(next_state.applied_speed, 180)


if __name__ == '__main__':
    main()
