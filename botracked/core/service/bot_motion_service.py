# -*- coding: UTF-8 -*-

'''
Module
    bot_motion_service.py
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
    Provides BotMotionService for commanding kinematic movements and robot actuators.
'''

from __future__ import annotations

from collections.abc import Callable

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.infrastructure.communication.binary_codec import (
    BinaryCodec,
)
from botracked.infrastructure.communication.serial_transport import (
    SerialTransport,
)
from botracked.infrastructure.communication.tcp_transport import (
    TcpTransport,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotMotionService:
    '''
        Defines class BotMotionService with attribute(s) and method(s).
        Controller service for sending kinematic and actuation frames to robot.

        It defines:

            :attributes:
                | _codec - Binary frame encoder/decoder.
                | _transport_provider - Supplier for currently active transport.
                | _on_tx - Observer notification callback for outgoing frames.
            :methods:
                | __init__ - Initializes motion service with injected dependencies.
                | _send_bytes - Sends binary payload over active transport.
                | send_motion - Dispatches manual motion jog command.
                | set_speed - Sets robot motor speed PWM.
                | stop_motors - Sends emergency or manual stop command.
                | ping - Sends ping message to verify link responsiveness.
                | clear_errors - Clears error state on the robot.
                | execute_step - Executes a single compiled mission step.
    '''

    _codec: BinaryCodec
    _transport_provider: Callable[[], SerialTransport | TcpTransport | None]
    _on_tx: Callable[[str, str, bytes], None]

    def __init__(
        self,
        codec: BinaryCodec,
        transport_provider: Callable[[], SerialTransport | TcpTransport | None],
        on_tx: Callable[[str, str, bytes], None],
    ) -> None:
        '''
            Initializes motion service with injected dependencies.

            :param codec: Binary frame encoder/decoder.
            :param transport_provider: Supplier for currently active transport.
            :param on_tx: Observer notification callback for outgoing frames.
            :exceptions: None.
        '''
        self._codec = codec
        self._transport_provider = transport_provider
        self._on_tx = on_tx

    def _send_bytes(self, payload: bytes, frame_name: str) -> bool:
        '''
            Sends binary payload over active transport and notifies observers.

            :param payload: Raw wire bytes.
            :param frame_name: Protocol command name.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        transport = self._transport_provider()
        if transport is None or not transport.is_connected():
            return False
        sent = transport.send(payload)
        if sent:
            self._on_tx('TX', frame_name, payload)
        return sent

    def send_motion(self, cmd: MotionCommand) -> bool:
        '''
            Dispatches manual motion jog command.

            :param cmd: Kinematic motion command.
            :return: True if dispatched, False on error.
            :exceptions: None.
        '''
        frame = self._codec.encode_frame(
            ProtocolOpcode.CMD_MOTION, bytes([cmd.value])
        )
        return self._send_bytes(frame, f'CMD_MOTION({cmd.name})')

    def set_speed(self, pwm: int) -> bool:
        '''
            Sets robot motor speed PWM.

            :param pwm: Speed value in range 0 to 255.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        clamped_pwm = max(0, min(255, pwm))
        frame = self._codec.encode_frame(
            ProtocolOpcode.CMD_SET_SPEED, bytes([clamped_pwm])
        )
        return self._send_bytes(frame, f'CMD_SET_SPEED({pwm})')

    def stop_motors(self) -> bool:
        '''
            Sends emergency or manual stop command.

            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_STOP)
        return self._send_bytes(frame, 'CMD_STOP')

    def ping(self) -> bool:
        '''
            Sends ping message to verify link responsiveness.

            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_PING)
        return self._send_bytes(frame, 'CMD_PING')

    def clear_errors(self) -> bool:
        '''
            Clears error state on the robot.

            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_ERR_CLEAR)
        return self._send_bytes(frame, 'CMD_ERR_CLEAR')

    def execute_step(self, step: CompiledStep) -> bool:
        '''
            Executes a single mission step.

            :param step: CompiledStep instance.
            :return: True if all frames dispatched, False otherwise.
            :exceptions: None.
        '''
        success: bool = True
        for frame in step.frames:
            desc: str = f'STEP L{step.line_number}: {step.description}'
            if not self._send_bytes(frame, desc):
                success = False
        return success
