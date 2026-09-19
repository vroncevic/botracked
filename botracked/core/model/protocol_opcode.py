# -*- coding: UTF-8 -*-

'''
Module
    protocol_opcode.py
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
    Defines ProtocolOpcode enumeration for binary framing protocol.
'''

from __future__ import annotations

from enum import IntEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProtocolOpcode(IntEnum):
    '''
        Binary protocol message IDs matching tracked_bot firmware packet definitions.

        It defines:

            :attributes:
                | CMD_MOTION - Opcode for kinematic motion jog command.
                | CMD_SET_SPEED - Opcode for motor PWM speed configuration.
                | CMD_STOP - Opcode for emergency or manual stop command.
                | CMD_PING - Opcode for heartbeat communication ping.
                | CMD_GET_STATUS - Opcode requesting operational telemetry status.
                | CMD_GET_DIAG - Opcode requesting detailed system diagnostics.
                | CMD_ERR_CLEAR - Opcode requesting clearing active error flags.
                | RESP_ACK - Opcode acknowledging successful command execution.
                | RESP_NACK - Opcode indicating rejected command or syntax error.
                | RESP_PONG - Opcode responding to link heartbeat ping.
                | RESP_STATUS - Opcode returning 7-byte operational telemetry report.
                | RESP_DIAG - Opcode returning 9-byte system diagnostics report.
            :methods:
                | is_response - Checks if opcode is an inbound response from the robot.
                | label - Returns human-readable mnemonic for the opcode.
    '''

    # Commands from Host to Robot
    CMD_MOTION = 0x01
    CMD_SET_SPEED = 0x02
    CMD_STOP = 0x03
    CMD_PING = 0x04
    CMD_GET_STATUS = 0x10
    CMD_GET_DIAG = 0x11
    CMD_ERR_CLEAR = 0x12

    # Responses from Robot to Host
    RESP_ACK = 0x80
    RESP_NACK = 0x81
    RESP_PONG = 0x84
    RESP_STATUS = 0x90
    RESP_DIAG = 0x91

    @property
    def is_response(self) -> bool:
        '''
            Checks if the opcode is an inbound response from the robot.

            :return: True if response, False if command.
            :exceptions: None.
        '''
        return bool(self.value & 0x80)

    @property
    def label(self) -> str:
        '''
            Returns human-readable mnemonic for the opcode.

            :return: Opcode label string.
            :exceptions: None.
        '''
        labels: dict[int, str] = {
            0x01: 'CMD_MOTION',
            0x02: 'CMD_SET_SPEED',
            0x03: 'CMD_STOP',
            0x04: 'CMD_PING',
            0x10: 'CMD_GET_STATUS',
            0x11: 'CMD_GET_DIAG',
            0x12: 'CMD_ERR_CLEAR',
            0x80: 'RESP_ACK',
            0x81: 'RESP_NACK',
            0x84: 'RESP_PONG',
            0x90: 'RESP_STATUS',
            0x91: 'RESP_DIAG',
        }

        return labels.get(self.value, f'0x{self.value:02X}')
