# -*- coding: UTF-8 -*-

'''
Module
    motion.py
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
    Defines MotionStepCompiler translating locomotion AST nodes to steps.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.dsl.compiler.node.state import SpeedState

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionStepCompiler:
    '''
        Defines class MotionStepCompiler implementing IMotionStepCompiler.
        Translates locomotion AST nodes into binary step sequences and speed transitions.

        It defines:

            :attributes:
                | ZERO_DURATION - Instantaneous step duration constant.
                | OVERRIDE_PARAM_COUNT - Parameter threshold for speed override.
                | _MOTION_MAP - Mapping from token types to MotionCommand enums.
                | _codec - Binary frame encoder and decoder port.
            :methods:
                | __init__ - Initializes motion compiler with binary codec port.
                | is_motion_token - Checks if token represents locomotion command.
                | compile_motion - Compiles locomotion AST node with SpeedState.
    '''

    ZERO_DURATION: ClassVar[float] = 0.0
    OVERRIDE_PARAM_COUNT: ClassVar[int] = 1

    _MOTION_MAP: ClassVar[MappingProxyType[TokenType, MotionCommand]] = (
        MappingProxyType({
            TokenType.FORWARD: MotionCommand.FORWARD,
            TokenType.BACKWARD: MotionCommand.BACKWARD,
            TokenType.TURN_LEFT: MotionCommand.TURN_LEFT,
            TokenType.TURN_RIGHT: MotionCommand.TURN_RIGHT,
            TokenType.SPIN_LEFT: MotionCommand.SPIN_LEFT,
            TokenType.SPIN_RIGHT: MotionCommand.SPIN_RIGHT,
        })
    )

    _codec: IBinaryCodec

    def __init__(self, codec: IBinaryCodec) -> None:
        '''
            Initializes motion compiler with binary codec port.

            :param codec: Binary frame codec port.
            :exceptions: None.
        '''
        self._codec = codec

    def is_motion_token(self, token_type: TokenType) -> bool:
        '''
            Checks if given token type represents a locomotion command.

            :param token_type: DSL token type to inspect.
            :return: True if token is locomotion command, False otherwise.
            :exceptions: None.
        '''
        return token_type in self._MOTION_MAP

    def compile_motion(
        self, node: AstInstruction, state: SpeedState
    ) -> tuple[CompiledStep, SpeedState]:
        '''
            Compiles locomotion AST node into executable CompiledStep and state.

            :param node: Locomotion AST instruction node.
            :param state: Current per-compilation speed state.
            :return: Tuple of CompiledStep and updated SpeedState.
            :exceptions: None.
        '''
        motion_cmd: MotionCommand = self._MOTION_MAP[node.token_type]
        dur: float = (
            node.parameters[0] if node.parameters else self.ZERO_DURATION
        )
        has_override: bool = len(node.parameters) > self.OVERRIDE_PARAM_COUNT
        target_speed: int = (
            int(node.parameters[1]) if has_override else state.current_speed
        )
        applied_speed: int = state.applied_speed
        frames_list: list[bytes] = []

        if has_override or target_speed != applied_speed:
            frames_list.append(
                self._codec.encode_frame(
                    ProtocolOpcode.CMD_SET_SPEED, bytes([target_speed])
                )
            )
            applied_speed = target_speed

        frames_list.append(
            self._codec.encode_frame(
                ProtocolOpcode.CMD_MOTION, bytes([motion_cmd.value])
            )
        )
        desc: str = node.token_type.name
        if dur > self.ZERO_DURATION:
            desc += f' for {dur:.1f}s'
        if has_override:
            desc += f' @ speed {target_speed}'

        step: CompiledStep = CompiledStep(
            frames=tuple(frames_list),
            duration_sec=dur,
            auto_stop_after=dur > self.ZERO_DURATION,
            description=desc,
            line_number=node.line_number,
        )
        next_state: SpeedState = SpeedState(
            current_speed=state.current_speed,
            applied_speed=applied_speed,
        )
        return step, next_state
