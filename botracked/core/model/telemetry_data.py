# -*- coding: UTF-8 -*-

'''
Module
    telemetry_data.py
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
    Defines TelemetryData value object holding tracked_bot runtime metrics.
'''

from __future__ import annotations

from dataclasses import dataclass
from time import time

from botracked.core.model.motion_command import MotionCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class TelemetryData:
    '''
        Immutable telemetry record received from tracked_bot.

        It defines:

            :attributes:
                | system_mode - Operating status mode (NORMAL, DEGRADED, PANIC, OFFLINE).
                | motion - Active kinematic MotionCommand enum member.
                | speed_pwm - Active PWM duty level [0, 255].
                | error_code - Diagnostic bitmask error byte.
                | uptime_ms - Time elapsed in milliseconds since connection started.
                | left_motor_state - Left motor actuator direction (FWD, REV, STOP).
                | right_motor_state - Right motor actuator direction (FWD, REV, STOP).
                | last_updated - Epoch timestamp of last received packet.
                | is_connected - True if physical link is established and active.
            :methods:
                | mode_str - Returns friendly string for system mode.
                | motion_cmd_str - Returns friendly string for motion command.
                | motor_left_str - Returns left motor state string.
                | motor_right_str - Returns right motor state string.
                | default_offline - Creates a default offline telemetry instance.
                | from_status_payload - Decodes binary status payload into TelemetryData.
    '''

    system_mode: str = 'OFFLINE'
    motion: MotionCommand = MotionCommand.STOP
    speed_pwm: int = 0
    error_code: int = 0
    uptime_ms: int = 0
    left_motor_state: str = 'STOP'
    right_motor_state: str = 'STOP'
    last_updated: float = 0.0
    is_connected: bool = False

    @property
    def mode_str(self) -> str:
        '''
            Returns friendly string for system mode.

            :return: String mode description.
            :exceptions: None.
        '''
        return self.system_mode

    @property
    def motion_cmd_str(self) -> str:
        '''
            Returns friendly string for motion command.

            :return: String motion label.
            :exceptions: None.
        '''
        return self.motion.label

    @property
    def motor_left_str(self) -> str:
        '''
            Returns left motor state string.

            :return: Left motor state string.
            :exceptions: None.
        '''
        return self.left_motor_state

    @property
    def motor_right_str(self) -> str:
        '''
            Returns right motor state string.

            :return: Right motor state string.
            :exceptions: None.
        '''
        return self.right_motor_state

    @classmethod
    def default_offline(cls) -> TelemetryData:
        '''
            Creates a default offline telemetry instance.

            :return: Default TelemetryData instance.
            :exceptions: None.
        '''
        return cls(
            system_mode='OFFLINE',
            motion=MotionCommand.STOP,
            speed_pwm=0,
            error_code=0,
            uptime_ms=0,
            left_motor_state='OFF',
            right_motor_state='OFF',
            last_updated=time(),
            is_connected=False,
        )

    @classmethod
    def from_status_payload(
        cls, payload: bytes, is_connected: bool = True, uptime_ms: int = 0
    ) -> TelemetryData:
        '''
            Decodes a binary RESP_STATUS (7B) or RESP_DIAG (9B) payload into TelemetryData.

            :param payload: Raw bytes payload from frame.
            :param is_connected: Connection state flag.
            :param uptime_ms: Optional elapsed connection time in milliseconds.
            :return: Parsed TelemetryData instance.
            :exceptions: None.
        '''
        if len(payload) < 4:
            return cls.default_offline()

        mode_map: dict[int, str] = {
            0: 'NORMAL',
            1: 'DEGRADED',
            2: 'PANIC',
        }
        mode_val: int = payload[0]
        mode_str: str = mode_map.get(mode_val, f'UNKNOWN({mode_val})')

        if len(payload) >= 7:
            err_code: int = payload[1]
            cmd_val: int = payload[5]
            speed: int = payload[6]
        else:
            cmd_val = payload[1]
            speed = payload[2]
            err_code = payload[3]

        try:
            motion: MotionCommand = MotionCommand(cmd_val)

        except ValueError:
            motion = MotionCommand.STOP

        left_state: str = 'STOP'
        right_state: str = 'STOP'

        match motion:
            case MotionCommand.FORWARD:
                left_state, right_state = 'FWD', 'FWD'
            case MotionCommand.BACKWARD:
                left_state, right_state = 'REV', 'REV'
            case MotionCommand.TURN_LEFT:
                left_state, right_state = 'STOP', 'FWD'
            case MotionCommand.TURN_RIGHT:
                left_state, right_state = 'FWD', 'STOP'
            case MotionCommand.SPIN_LEFT:
                left_state, right_state = 'REV', 'FWD'
            case MotionCommand.SPIN_RIGHT:
                left_state, right_state = 'FWD', 'REV'
            case _:
                left_state, right_state = 'STOP', 'STOP'

        return cls(
            system_mode=mode_str,
            motion=motion,
            speed_pwm=speed,
            error_code=err_code,
            uptime_ms=uptime_ms,
            left_motor_state=left_state,
            right_motor_state=right_state,
            last_updated=time(),
            is_connected=is_connected,
        )
