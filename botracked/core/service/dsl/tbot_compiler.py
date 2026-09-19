# -*- coding: UTF-8 -*-

'''
Module
    tbot_compiler.py
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
    Provides TbotCompiler transforming AST nodes into executable binary frames.
'''

from __future__ import annotations

from botracked.core.model.dsl.ast_instruction import AstInstruction
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.dsl.token_type import TokenType
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.infrastructure.communication.binary_codec import BinaryCodec

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TbotCompiler:
    '''
        Defines class TbotCompiler with attribute(s) and method(s).
        Compiles mission script AST instructions into timed binary frame sequences.

        It defines:

            :attributes:
                | _codec - Binary packet encoder/decoder.
                | _current_speed - Current locomotion speed setting.
                | _MOTION_MAP - Mapping from motion TokenType to MotionCommand enum.
            :methods:
                | __init__ - Initializes compiler with binary packet codec.
                | compile - Compiles AST instruction list into binary steps.
                | estimate_duration - Estimates total execution duration in seconds.
                | _compile_nodes - Recursively compiles AST nodes into steps.
    '''

    _codec: BinaryCodec
    _current_speed: int

    _MOTION_MAP: dict[TokenType, MotionCommand] = {
        TokenType.FORWARD: MotionCommand.FORWARD,
        TokenType.BACKWARD: MotionCommand.BACKWARD,
        TokenType.TURN_LEFT: MotionCommand.TURN_LEFT,
        TokenType.TURN_RIGHT: MotionCommand.TURN_RIGHT,
        TokenType.SPIN_LEFT: MotionCommand.SPIN_LEFT,
        TokenType.SPIN_RIGHT: MotionCommand.SPIN_RIGHT,
    }

    def __init__(self, codec: BinaryCodec | None = None) -> None:
        '''
            Initializes compiler with binary packet codec.

            :param codec: Optional BinaryCodec instance.
            :exceptions: None.
        '''
        self._codec = codec if codec is not None else BinaryCodec()
        self._current_speed = 180

    def compile(self, ast: list[AstInstruction]) -> list[CompiledStep]:
        '''
            Compiles AST instruction list into executable binary steps.

            :param ast: List of parsed AstInstruction nodes.
            :return: Ordered list of CompiledStep instances.
            :exceptions: None.
        '''
        steps: list[CompiledStep] = []
        self._compile_nodes(ast, steps)

        return steps

    def estimate_duration(self, ast: list[AstInstruction]) -> float:
        '''
            Estimates total execution duration in seconds for given AST instructions.

            :param ast: List of parsed AstInstruction nodes.
            :return: Estimated execution time in seconds.
            :exceptions: None.
        '''
        steps: list[CompiledStep] = self.compile(ast)

        return sum(step.duration_sec for step in steps)

    def _compile_nodes(
        self, nodes: list[AstInstruction] | tuple[AstInstruction, ...], steps: list[CompiledStep]
    ) -> None:
        '''
            Recursively compiles AST nodes into executable steps.

            :param nodes: Sequence of AST instruction nodes.
            :param steps: Accumulator list for compiled steps.
            :exceptions: None.
        '''
        for node in nodes:
            if node.token_type == TokenType.SPEED:
                spd: int = int(node.param1) if node.param1 is not None else 180
                self._current_speed = spd
                frame: bytes = self._codec.encode_frame(
                    ProtocolOpcode.CMD_SET_SPEED, bytes([spd])
                )
                steps.append(CompiledStep(
                    frames=(frame,),
                    duration_sec=0.0,
                    auto_stop_after=False,
                    description=f'SET SPEED {spd}',
                    line_number=node.line_number,
                ))

            elif node.token_type in self._MOTION_MAP:
                motion_cmd: MotionCommand = self._MOTION_MAP[node.token_type]
                frames_list: list[bytes] = []
                dur: float = float(node.param1) if node.param1 is not None else 0.0
                spd_override: int | None = int(node.param2) if node.param2 is not None else None

                if spd_override is not None:
                    frames_list.append(
                        self._codec.encode_frame(
                            ProtocolOpcode.CMD_SET_SPEED, bytes([spd_override])
                        )
                    )

                frames_list.append(
                    self._codec.encode_frame(
                        ProtocolOpcode.CMD_MOTION, bytes([motion_cmd.value])
                    )
                )

                auto_stop: bool = dur > 0.0
                desc: str = f'{node.token_type.name}'

                if dur > 0.0:
                    desc += f' for {dur:.1f}s'

                if spd_override is not None:
                    desc += f' @ speed {spd_override}'

                steps.append(CompiledStep(
                    frames=tuple(frames_list),
                    duration_sec=dur,
                    auto_stop_after=auto_stop,
                    description=desc,
                    line_number=node.line_number,
                ))

            elif node.token_type == TokenType.WAIT:
                dur = float(node.param1) if node.param1 is not None else 0.5
                steps.append(CompiledStep(
                    frames=(),
                    duration_sec=dur,
                    auto_stop_after=False,
                    description=f'WAIT {dur:.1f}s',
                    line_number=node.line_number,
                ))

            elif node.token_type == TokenType.STOP:
                frame = self._codec.encode_frame(ProtocolOpcode.CMD_STOP)
                steps.append(CompiledStep(
                    frames=(frame,),
                    duration_sec=0.0,
                    auto_stop_after=False,
                    description='STOP',
                    line_number=node.line_number,
                ))

            elif node.token_type == TokenType.PING:
                frame = self._codec.encode_frame(ProtocolOpcode.CMD_PING)
                steps.append(CompiledStep(
                    frames=(frame,),
                    duration_sec=0.0,
                    auto_stop_after=False,
                    description='PING',
                    line_number=node.line_number,
                ))

            elif node.token_type == TokenType.CLEAR_ERRORS:
                frame = self._codec.encode_frame(ProtocolOpcode.CMD_ERR_CLEAR)
                steps.append(CompiledStep(
                    frames=(frame,),
                    duration_sec=0.0,
                    auto_stop_after=False,
                    description='CLEAR_ERRORS',
                    line_number=node.line_number,
                ))

            elif node.token_type == TokenType.REPEAT:
                count: int = int(node.param1) if node.param1 is not None else 1

                for _ in range(count):
                    self._compile_nodes(node.children, steps)
