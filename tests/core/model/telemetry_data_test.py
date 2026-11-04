# -*- coding: UTF-8 -*-

'''
Module
    telemetry_data_test.py
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
    Unit tests for TelemetryData model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.telemetry_data import TelemetryData

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryDataTest(TestCase):
    '''
        Tests TelemetryData initialization, attributes, immutability, and equality.
    '''

    def test_instantiation_and_fields(self) -> None:
        '''
            Verifies field values upon standard instantiation.

            :exceptions: None.
        '''
        telemetry = TelemetryData(
            system_mode='NORMAL',
            motion=MotionCommand.FORWARD,
            speed_pwm=180,
            error_code=0,
            uptime_ms=12500,
            left_motor_state='FWD',
            right_motor_state='FWD',
            last_updated=1700000000.0,
            is_connected=True
        )
        self.assertEqual(telemetry.system_mode, 'NORMAL')
        self.assertEqual(telemetry.motion, MotionCommand.FORWARD)
        self.assertEqual(telemetry.speed_pwm, 180)
        self.assertEqual(telemetry.error_code, 0)
        self.assertEqual(telemetry.uptime_ms, 12500)
        self.assertEqual(telemetry.left_motor_state, 'FWD')
        self.assertEqual(telemetry.right_motor_state, 'FWD')
        self.assertEqual(telemetry.last_updated, 1700000000.0)
        self.assertTrue(telemetry.is_connected)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying frozen dataclass attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        telemetry = TelemetryData(
            system_mode='OFFLINE',
            motion=MotionCommand.STOP,
            speed_pwm=0,
            error_code=0,
            uptime_ms=0,
            left_motor_state='OFF',
            right_motor_state='OFF',
            last_updated=0.0,
            is_connected=False
        )
        with self.assertRaises(FrozenInstanceError):
            telemetry.is_connected = True  # type: ignore[misc]

    def test_equality(self) -> None:
        '''
            Verifies equality comparison between TelemetryData instances.

            :exceptions: None.
        '''
        t1 = TelemetryData('NORMAL', MotionCommand.STOP, 0, 0, 100, 'OFF', 'OFF', 1.0, True)
        t2 = TelemetryData('NORMAL', MotionCommand.STOP, 0, 0, 100, 'OFF', 'OFF', 1.0, True)
        t3 = TelemetryData('PANIC', MotionCommand.STOP, 0, 1, 100, 'OFF', 'OFF', 1.0, True)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)


if __name__ == '__main__':
    main()
