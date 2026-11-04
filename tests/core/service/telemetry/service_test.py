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
    Unit tests for BotTelemetryService observer registry and fanout.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.telemetry.protocol.iobserver import ITelemetryObserver
from botracked.core.service.telemetry.service import BotTelemetryService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotTelemetryServiceTestCase(TestCase):
    '''
        Verifies BotTelemetryService observer registration and event fanout.
    '''

    def test_add_remove_and_notify_telemetry(self) -> None:
        '''
            Verifies observer registration deduplication and telemetry fanout.

            :exceptions: None.
        '''
        service = BotTelemetryService()
        obs1 = Mock(spec=ITelemetryObserver)
        obs2 = Mock(spec=ITelemetryObserver)
        service.add_observer(obs1)
        service.add_observer(obs1)
        service.add_observer(obs2)

        data = TelemetryData(
            system_mode='NORMAL',
            motion=MotionCommand.STOP,
            speed_pwm=100,
            error_code=0,
            uptime_ms=1234,
            left_motor_state='STOP',
            right_motor_state='STOP',
            last_updated=1000.0,
            is_connected=True,
        )
        service.notify_telemetry(data)
        obs1.on_telemetry.assert_called_once_with(data)
        obs2.on_telemetry.assert_called_once_with(data)

        service.remove_observer(obs1)
        service.remove_observer(obs1)
        service.notify_packet(PacketDirection.TX, 'PING', b'\xaa')
        obs1.on_packet.assert_not_called()
        obs2.on_packet.assert_called_once_with(
            PacketDirection.TX, 'PING', b'\xaa'
        )


if __name__ == '__main__':
    main()
