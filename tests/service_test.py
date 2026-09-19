# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Unit tests for BotService facade and segregated sub-services.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.model.motion_command import MotionCommand
from botracked.core.service.bot_service import BotService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestService(TestCase):
    '''
    Tests BotService initialization, sub-service wiring, and offline behavior.
    '''

    _service: BotService

    def setUp(self) -> None:
        self._service = BotService()

    def test_service_initialization(self) -> None:
        '''
        Verifies all sub-services and workers are initialized.
        '''
        self.assertTrue(self._service.is_initialized())
        self.assertIsNotNone(self._service.get_motion())
        self.assertIsNotNone(self._service.get_telemetry())
        self.assertIsNotNone(self._service.get_mission_runner())
        self.assertFalse(self._service.is_connected())

    def test_offline_motion_rejection(self) -> None:
        '''
        Verifies motion command returns False when transport is disconnected.
        '''
        motion = self._service.get_motion()
        sent = motion.send_motion(MotionCommand.FORWARD)
        self.assertFalse(sent)

    def test_offline_execute_step(self) -> None:
        '''
        Verifies step execution returns False without error when offline.
        '''
        motion = self._service.get_motion()
        step = CompiledStep(
            frames=(b'\xaa\x01\x01\x01\x79',),
            duration_sec=1.0,
            auto_stop_after=True,
            description='FORWARD for 1.0s',
            line_number=5,
        )
        sent = motion.execute_step(step)
        self.assertFalse(sent)

    def test_telemetry_snapshot(self) -> None:
        '''
        Verifies default offline telemetry state.
        '''
        telem = self._service.get_telemetry().get_telemetry()
        self.assertEqual(telem.system_mode, 'OFFLINE')
        self.assertEqual(telem.speed_pwm, 0)


if __name__ == '__main__':
    main()
