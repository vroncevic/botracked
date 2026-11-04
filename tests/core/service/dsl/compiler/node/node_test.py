# -*- coding: UTF-8 -*-

'''
Module
    node_test.py
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
    Unit tests for NodeCompiler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
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


class NodeCompilerTest(TestCase):
    '''
        Defines test methods for NodeCompiler behavior.
    '''

    _mock_codec: Mock
    _node_compiler: NodeCompiler

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self._mock_codec = Mock(spec=IBinaryCodec)
        self._mock_codec.encode_frame.side_effect = (
            lambda opcode, payload: bytes([int(opcode)]) + payload
        )
        motion_compiler = MotionStepCompiler(codec=self._mock_codec)
        self._node_compiler = NodeCompiler(
            motion_compiler=motion_compiler,
            codec=self._mock_codec,
            default_speed=180,
        )

    def test_speed_compilation_and_reset(self) -> None:
        '''
            Verifies SPEED frame generation and initial_state baseline speed.

            :exceptions: None.
        '''
        steps: list[CompiledStep] = []
        state = self._node_compiler.initial_state()
        state = self._node_compiler.compile_node(
            AstInstruction(TokenType.SPEED, 1, (200.0,), ()), steps, state
        )
        self.assertEqual(steps[0].description, 'SET SPEED 200')
        self.assertEqual(
            steps[0].frames,
            (bytes([int(ProtocolOpcode.CMD_SET_SPEED), 200]),),
        )

        fresh = self._node_compiler.initial_state()
        fresh = self._node_compiler.compile_node(
            AstInstruction(TokenType.FORWARD, 2, (1.0, 220.0), ()), steps, fresh
        )
        self._node_compiler.compile_node(
            AstInstruction(TokenType.BACKWARD, 3, (), ()), steps, fresh
        )
        self.assertEqual(
            steps[2].frames[0],
            bytes([int(ProtocolOpcode.CMD_SET_SPEED), 180]),
        )

    def test_motion_override_and_speed_restoration(self) -> None:
        '''
            Verifies motion override emits CMD_SET_SPEED and restores speed next step.

            :exceptions: None.
        '''
        steps: list[CompiledStep] = []
        state = self._node_compiler.initial_state()
        state = self._node_compiler.compile_node(
            AstInstruction(TokenType.FORWARD, 1, (2.5, 240.0), ()), steps, state
        )
        self.assertEqual(len(steps[0].frames), 2)
        self.assertTrue(steps[0].auto_stop_after)
        self.assertIn('@ speed 240', steps[0].description)

        state = self._node_compiler.compile_node(
            AstInstruction(TokenType.BACKWARD, 2, (), ()), steps, state
        )
        self.assertEqual(len(steps[1].frames), 2)
        self.assertFalse(steps[1].auto_stop_after)

        self._node_compiler.compile_node(
            AstInstruction(TokenType.FORWARD, 3, (1.0,), ()), steps, state
        )
        self.assertEqual(len(steps[2].frames), 1)

    def test_wait_simple_repeat_and_unsupported(self) -> None:
        '''
            Verifies WAIT, STOP, PING, CLEAR_ERRORS, REPEAT, and syntax errors.

            :exceptions: None.
        '''
        steps: list[CompiledStep] = []
        state = self._node_compiler.initial_state()
        wait_node = AstInstruction(TokenType.WAIT, 1, (1.5,), ())
        stop_node = AstInstruction(TokenType.STOP, 2, (), ())
        ping_node = AstInstruction(TokenType.PING, 3, (), ())
        clear_node = AstInstruction(TokenType.CLEAR_ERRORS, 4, (), ())
        fwd_node = AstInstruction(TokenType.FORWARD, 6, (2.0,), ())
        rep_node = AstInstruction(TokenType.REPEAT, 5, (3.0,), (fwd_node, stop_node))

        for inst in (wait_node, stop_node, ping_node, clear_node, rep_node):
            state = self._node_compiler.compile_node(inst, steps, state)

        self.assertEqual(len(steps), 10)

        bad_node = AstInstruction(TokenType.IDENTIFIER, 7, (), ())
        with self.assertRaises(DslSyntaxError):
            self._node_compiler.compile_node(bad_node, steps, state)


if __name__ == '__main__':
    main()
