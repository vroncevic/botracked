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
    Defines BotMotionService managing kinematics and mission step dispatch.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotMotionService:
    '''
        Defines class BotMotionService implementing IBotMotionService structurally.
        Controller service commanding kinematic movements, speed, and mission steps.

        It defines:

            :attributes:
                | MIN_PWM - Minimum clamped PWM duty cycle byte value.
                | MAX_PWM - Maximum clamped PWM duty cycle byte value.
                | _dispatcher - Frame dispatcher for encoding and link delivery.
            :methods:
                | __init__ - Initializes motion service with injected dispatcher.
                | send_motion - Dispatches manual motion jog command.
                | set_speed - Sets robot motor speed PWM.
                | stop_motors - Sends emergency or manual stop command.
                | send_command - Dispatches zero-payload control opcode frame.
                | execute_step - Executes a single compiled mission step.
    '''

    MIN_PWM: ClassVar[int] = 0
    MAX_PWM: ClassVar[int] = 255

    _dispatcher: IFrameDispatcher

    def __init__(self, dispatcher: IFrameDispatcher) -> None:
        '''
            Initializes motion service with injected frame dispatcher.

            :param dispatcher: Dispatcher handling frame encoding and transmission.
            :exceptions: None.
        '''
        self._dispatcher = dispatcher

    def send_motion(self, cmd: MotionCommand) -> bool:
        '''
            Dispatches manual motion jog command.

            :param cmd: Kinematic motion command.
            :return: True if dispatched, False on error.
            :exceptions: None.
        '''
        return self._dispatcher.dispatch_frame(
            ProtocolOpcode.CMD_MOTION,
            bytes([cmd.value]),
            f'CMD_MOTION({cmd.name})',
        )

    def set_speed(self, pwm: int) -> bool:
        '''
            Sets robot motor speed PWM.

            :param pwm: Speed value in range 0 to 255.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        clamped_pwm = max(self.MIN_PWM, min(self.MAX_PWM, pwm))

        return self._dispatcher.dispatch_frame(
            ProtocolOpcode.CMD_SET_SPEED,
            bytes([clamped_pwm]),
            f'CMD_SET_SPEED({pwm})',
        )

    def stop_motors(self) -> bool:
        '''
            Sends emergency or manual stop command.

            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self.send_command(ProtocolOpcode.CMD_STOP)

    def send_command(self, opcode: ProtocolOpcode) -> bool:
        '''
            Dispatches zero-payload control or diagnostic opcode frame.

            :param opcode: ProtocolOpcode command value.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        return self._dispatcher.dispatch_frame(opcode, b'', opcode.name)

    def execute_step(self, step: CompiledStep) -> bool:
        '''
            Executes a single compiled mission step.

            :param step: CompiledStep instance with binary frames.
            :return: True if all frames dispatched, False otherwise.
            :exceptions: None.
        '''
        success: bool = True

        for frame in step.frames:
            desc: str = f'STEP L{step.line_number}: {step.description}'

            if not self._dispatcher.dispatch_raw(frame, desc):
                success = False

        return success
