# -*- coding: UTF-8 -*-

'''
Module
    inspector.py
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
    Defines TelemetryInspector implementing ITelemetryInspector structurally.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.motor_state import MotorState
from botracked.core.model.system_mode import SystemMode
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.concurrency.iclock import IClock

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryInspector:
    '''
        Defines class TelemetryInspector implementing ITelemetryInspector.
        Provides telemetry payload decoding, offline creation, and formatting.

        It defines:

            :attributes:
                | MIN_STATUS_LEN - Minimum byte length for compact status payload.
                | MIN_DIAG_LEN - Minimum byte length for extended diagnostic payload.
                | ZERO_VALUE - Default numeric reset value for offline telemetry.
                | RAW_SEPARATOR - Raw enum separator character in motion names.
                | LABEL_SEPARATOR - Friendly label separator character.
                | _MODE_MAP - Mapping from wire mode integers to SystemMode strings.
                | _MOTOR_STATES - Mapping from MotionCommand to (left, right) states.
                | _clock - Wall-clock time source port stamping snapshots.
            :methods:
                | __init__ - Initializes TelemetryInspector with clock port.
                | create_offline - Creates default offline TelemetryData record.
                | decode_payload - Decodes binary status payload into TelemetryData.
                | motion_label - Formats motion command into friendly label.
    '''

    MIN_STATUS_LEN: ClassVar[int] = 4
    MIN_DIAG_LEN: ClassVar[int] = 7
    ZERO_VALUE: ClassVar[int] = 0
    RAW_SEPARATOR: ClassVar[str] = '_'
    LABEL_SEPARATOR: ClassVar[str] = ' '

    _MODE_MAP: ClassVar[MappingProxyType[int, str]] = MappingProxyType({
        0: SystemMode.NORMAL.value,
        1: SystemMode.DEGRADED.value,
        2: SystemMode.PANIC.value,
    })

    _MOTOR_STATES: ClassVar[MappingProxyType[MotionCommand, tuple[str, str]]] = (
        MappingProxyType({
            MotionCommand.FORWARD: (MotorState.FWD.value, MotorState.FWD.value),
            MotionCommand.BACKWARD: (MotorState.REV.value, MotorState.REV.value),
            MotionCommand.TURN_LEFT: (MotorState.STOP.value, MotorState.FWD.value),
            MotionCommand.TURN_RIGHT: (MotorState.FWD.value, MotorState.STOP.value),
            MotionCommand.SPIN_LEFT: (MotorState.REV.value, MotorState.FWD.value),
            MotionCommand.SPIN_RIGHT: (MotorState.FWD.value, MotorState.REV.value),
        })
    )

    _clock: IClock

    def __init__(self, clock: IClock) -> None:
        '''
            Initializes TelemetryInspector with wall-clock time source port.

            :param clock: Wall-clock time source port.
            :exceptions: None.
        '''
        self._clock = clock

    def create_offline(self) -> TelemetryData:
        '''
            Creates default offline TelemetryData record.

            :return: Default offline TelemetryData instance.
            :exceptions: None.
        '''
        return TelemetryData(
            system_mode=SystemMode.OFFLINE.value,
            motion=MotionCommand.STOP,
            speed_pwm=self.ZERO_VALUE,
            error_code=self.ZERO_VALUE,
            uptime_ms=self.ZERO_VALUE,
            left_motor_state=MotorState.OFF.value,
            right_motor_state=MotorState.OFF.value,
            last_updated=self._clock.now(),
            is_connected=False,
        )

    def decode_payload(
        self, payload: bytes, *, is_connected: bool, uptime_ms: int
    ) -> TelemetryData:
        '''
            Decodes binary status payload into TelemetryData.

            :param payload: Raw bytes payload from status or diagnostic frame.
            :param is_connected: Connection state flag.
            :param uptime_ms: Connection elapsed time in milliseconds.
            :return: Decoded TelemetryData instance.
            :exceptions: None.
        '''
        if len(payload) < self.MIN_STATUS_LEN:
            return self.create_offline()

        mode_val: int = payload[0]
        mode_str: str = self._MODE_MAP.get(
            mode_val, f'{SystemMode.UNKNOWN.value}({mode_val})'
        )

        if len(payload) >= self.MIN_DIAG_LEN:
            err_code, cmd_val, speed = payload[1], payload[5], payload[6]
        else:
            cmd_val, speed, err_code = payload[1], payload[2], payload[3]

        try:
            motion: MotionCommand = MotionCommand(cmd_val)
        except ValueError:
            motion = MotionCommand.STOP

        left_state, right_state = self._MOTOR_STATES.get(
            motion, (MotorState.STOP.value, MotorState.STOP.value)
        )

        return TelemetryData(
            system_mode=mode_str,
            motion=motion,
            speed_pwm=speed,
            error_code=err_code,
            uptime_ms=uptime_ms,
            left_motor_state=left_state,
            right_motor_state=right_state,
            last_updated=self._clock.now(),
            is_connected=is_connected,
        )

    def motion_label(self, telemetry: TelemetryData) -> str:
        '''
            Formats motion command into friendly label.

            :param telemetry: TelemetryData instance to format.
            :return: Friendly motion label string.
            :exceptions: None.
        '''
        return telemetry.motion.name.replace(
            self.RAW_SEPARATOR, self.LABEL_SEPARATOR
        )
