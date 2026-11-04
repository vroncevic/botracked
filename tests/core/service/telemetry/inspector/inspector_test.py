# -*- coding: UTF-8 -*-

'''
Module
    inspector_test.py
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
    Unit tests for TelemetryInspector.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.motor_state import MotorState
from botracked.core.model.system_mode import SystemMode
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.inspector.inspector import TelemetryInspector

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryInspectorTest(TestCase):
    '''
        Defines test methods for TelemetryInspector behavior.
    '''

    _clock: Mock
    _inspector: TelemetryInspector

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self._clock = Mock(spec=IClock)
        self._clock.now.return_value = 1700000000.0
        self._inspector = TelemetryInspector(clock=self._clock)

    def test_protocol_and_offline(self) -> None:
        '''
            Verifies structural protocol conformance and offline snapshot.

            :exceptions: None.
        '''
        self.assertIsInstance(self._inspector, ITelemetryInspector)
        offline = self._inspector.create_offline()
        self.assertEqual(offline.system_mode, SystemMode.OFFLINE)
        self.assertEqual(offline.motion, MotionCommand.STOP)
        self.assertEqual(offline.left_motor_state, MotorState.OFF)
        self.assertEqual(offline.last_updated, 1700000000.0)
        self.assertFalse(offline.is_connected)
        short = self._inspector.decode_payload(
            b'\x01\x02', is_connected=True, uptime_ms=10
        )
        self.assertFalse(short.is_connected)

    def test_decode_7_byte_and_4_byte_payloads(self) -> None:
        '''
            Verifies 7-byte and 4-byte binary status payload decoding.

            :exceptions: None.
        '''
        data_normal = self._inspector.decode_payload(
            bytes([0, 10, 0, 0, 0, 1, 180]),
            is_connected=True,
            uptime_ms=500,
        )
        self.assertEqual(data_normal.system_mode, SystemMode.NORMAL)
        self.assertEqual(data_normal.error_code, 10)
        self.assertEqual(data_normal.motion, MotionCommand.FORWARD)
        self.assertEqual(data_normal.speed_pwm, 180)
        self.assertEqual(data_normal.uptime_ms, 500)

        data_4b = self._inspector.decode_payload(
            bytes([1, 2, 120, 7]),
            is_connected=True,
            uptime_ms=300,
        )
        self.assertEqual(data_4b.system_mode, SystemMode.DEGRADED)
        self.assertEqual(data_4b.motion, MotionCommand.BACKWARD)
        self.assertEqual(data_4b.error_code, 7)

    def test_motor_states_and_unknown_values(self) -> None:
        '''
            Verifies motor state mapping, unknown modes, and motion labels.

            :exceptions: None.
        '''
        for cmd_code, expected_left, expected_right in (
            (2, MotorState.REV, MotorState.REV),
            (3, MotorState.STOP, MotorState.FWD),
            (4, MotorState.FWD, MotorState.STOP),
            (5, MotorState.REV, MotorState.FWD),
            (6, MotorState.FWD, MotorState.REV),
            (250, MotorState.STOP, MotorState.STOP),
        ):
            snap = self._inspector.decode_payload(
                bytes([2, 0, 0, 0, 0, cmd_code, 100]),
                is_connected=True,
                uptime_ms=100,
            )
            self.assertEqual(snap.left_motor_state, expected_left)
            self.assertEqual(snap.right_motor_state, expected_right)

        unknown_mode = self._inspector.decode_payload(
            bytes([99, 0, 0, 0, 0, 3, 100]),
            is_connected=True,
            uptime_ms=50,
        )
        self.assertEqual(unknown_mode.system_mode, 'UNKNOWN(99)')
        self.assertEqual(self._inspector.motion_label(unknown_mode), 'TURN LEFT')


if __name__ == '__main__':
    main()
