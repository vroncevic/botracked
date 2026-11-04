# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines IBotMotionService structural protocol interface.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.protocol_opcode import ProtocolOpcode

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBotMotionService(Protocol):
    '''
        Defines protocol IBotMotionService with method(s).
        Provides an interface for driving robot locomotion and control opcodes.

        It defines:

            :methods:
                | send_motion - Dispatches manual motion jog command.
                | set_speed - Sets robot motor speed PWM.
                | stop_motors - Sends emergency or manual stop command.
                | send_command - Dispatches zero-payload control opcode frame.
                | execute_step - Executes a single compiled mission step.
    '''

    def send_motion(self, cmd: MotionCommand) -> bool:
        '''
            Dispatches manual motion jog command.

            :param cmd: Kinematic motion command.
            :return: True if dispatched, False on error.
        '''

    def set_speed(self, pwm: int) -> bool:
        '''
            Sets robot motor speed PWM.

            :param pwm: Speed value in range 0 to 255.
            :return: True if sent, False otherwise.
        '''

    def stop_motors(self) -> bool:
        '''
            Sends emergency or manual stop command.

            :return: True if sent, False otherwise.
        '''

    def send_command(self, opcode: ProtocolOpcode) -> bool:
        '''
            Dispatches zero-payload control or diagnostic opcode frame.

            :param opcode: ProtocolOpcode command value.
            :return: True if sent, False otherwise.
        '''

    def execute_step(self, step: CompiledStep) -> bool:
        '''
            Executes a single mission step.

            :param step: CompiledStep instance.
            :return: True if all frames dispatched, False otherwise.
        '''
