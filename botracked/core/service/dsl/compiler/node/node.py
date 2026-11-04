# -*- coding: UTF-8 -*-

'''
Module
    node.py
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
    Defines stateless NodeCompiler translating AST nodes into CompiledSteps.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.exceptions.dsl_syntax_error import DslSyntaxError
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.motion.imotion import IMotionStepCompiler
from botracked.core.service.dsl.compiler.node.state import SpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NodeCompiler:
    '''
        Defines class NodeCompiler implementing INodeCompiler structurally.
        Stateless recursive compiler threading SpeedState across AST nodes.

        It defines:

            :attributes:
                | ZERO_DURATION - Instantaneous step duration constant.
                | DEFAULT_WAIT_SEC - Fallback wait duration when omitted.
                | DEFAULT_REPEAT_COUNT - Fallback loop iteration count.
                | _SIMPLE_OPCODES - Mapping from simple command tokens to opcodes.
                | _motion_compiler - Locomotion step compiler port.
                | _codec - Binary frame encoder and decoder port.
                | _default_speed - Configured baseline locomotion speed.
            :methods:
                | __init__ - Initializes node compiler with collaborators.
                | initial_state - Creates baseline SpeedState for compilation run.
                | compile_node - Compiles AST node into steps and returns state.
    '''

    ZERO_DURATION: ClassVar[float] = 0.0
    DEFAULT_WAIT_SEC: ClassVar[float] = 0.5
    DEFAULT_REPEAT_COUNT: ClassVar[int] = 1

    _SIMPLE_OPCODES: ClassVar[MappingProxyType[TokenType, ProtocolOpcode]] = (
        MappingProxyType({
            TokenType.STOP: ProtocolOpcode.CMD_STOP,
            TokenType.PING: ProtocolOpcode.CMD_PING,
            TokenType.CLEAR_ERRORS: ProtocolOpcode.CMD_ERR_CLEAR,
        })
    )

    _motion_compiler: IMotionStepCompiler
    _codec: IBinaryCodec
    _default_speed: int

    def __init__(
        self,
        *,
        motion_compiler: IMotionStepCompiler,
        codec: IBinaryCodec,
        default_speed: int,
    ) -> None:
        '''
            Initializes node compiler with motion compiler and codec ports.

            :param motion_compiler: Locomotion step compiler collaborator.
            :param codec: Binary frame codec port.
            :param default_speed: Baseline locomotion speed integer (0..255).
            :exceptions: None.
        '''
        self._motion_compiler = motion_compiler
        self._codec = codec
        self._default_speed = default_speed

    def initial_state(self) -> SpeedState:
        '''
            Creates baseline SpeedState initialized to default speed.

            :return: Initial SpeedState instance.
            :exceptions: None.
        '''
        return SpeedState(
            current_speed=self._default_speed,
            applied_speed=self._default_speed,
        )

    def compile_node(
        self,
        node: AstInstruction,
        steps: list[CompiledStep],
        state: SpeedState,
    ) -> SpeedState:
        '''
            Compiles a single AST node into executable steps and returns state.

            :param node: AST instruction node to compile.
            :param steps: Accumulator list for generated CompiledStep instances.
            :param state: Current per-compilation speed state.
            :return: Updated SpeedState after compiling node.
            :exceptions:
                | DslSyntaxError: If node token type is unsupported.
        '''
        match node.token_type:
            case TokenType.SPEED:
                spd: int = (
                    int(node.parameters[0])
                    if node.parameters
                    else self._default_speed
                )
                frame: bytes = self._codec.encode_frame(
                    ProtocolOpcode.CMD_SET_SPEED, bytes([spd])
                )
                steps.append(CompiledStep(
                    frames=(frame,),
                    duration_sec=self.ZERO_DURATION,
                    auto_stop_after=False,
                    description=f'SET SPEED {spd}',
                    line_number=node.line_number,
                ))
                return SpeedState(current_speed=spd, applied_speed=spd)
            case _ if self._motion_compiler.is_motion_token(node.token_type):
                step, next_state = self._motion_compiler.compile_motion(
                    node, state
                )
                steps.append(step)
                return next_state
            case TokenType.WAIT:
                dur: float = (
                    node.parameters[0]
                    if node.parameters
                    else self.DEFAULT_WAIT_SEC
                )
                steps.append(CompiledStep(
                    frames=(),
                    duration_sec=dur,
                    auto_stop_after=False,
                    description=f'WAIT {dur:.1f}s',
                    line_number=node.line_number,
                ))
                return state
            case TokenType.STOP | TokenType.PING | TokenType.CLEAR_ERRORS:
                opcode: ProtocolOpcode = self._SIMPLE_OPCODES[node.token_type]
                simple_frame: bytes = self._codec.encode_frame(opcode, b'')
                steps.append(CompiledStep(
                    frames=(simple_frame,),
                    duration_sec=self.ZERO_DURATION,
                    auto_stop_after=False,
                    description=node.token_type.name,
                    line_number=node.line_number,
                ))
                return state
            case TokenType.REPEAT:
                count: int = (
                    int(node.parameters[0])
                    if node.parameters
                    else self.DEFAULT_REPEAT_COUNT
                )
                cur_state: SpeedState = state
                for _ in range(count):
                    for child in node.children:
                        cur_state = self.compile_node(child, steps, cur_state)
                return cur_state
            case _:
                raise DslSyntaxError(
                    f'Line {node.line_number}: Unsupported AST node '
                    f'{node.token_type.name}'
                )
