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

from botracked.core.model.motion_command import MotionCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
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
                | speed_pwm - Active PWM duty level in range [0, 255].
                | error_code - Diagnostic bitmask error byte.
                | uptime_ms - Time elapsed in milliseconds since connection started.
                | left_motor_state - Left motor actuator direction (FWD, REV, STOP, OFF).
                | right_motor_state - Right motor actuator direction (FWD, REV, STOP, OFF).
                | last_updated - Epoch timestamp of last received packet.
                | is_connected - True if physical link is established and active.
    '''

    system_mode: str
    motion: MotionCommand
    speed_pwm: int
    error_code: int
    uptime_ms: int
    left_motor_state: str
    right_motor_state: str
    last_updated: float
    is_connected: bool
