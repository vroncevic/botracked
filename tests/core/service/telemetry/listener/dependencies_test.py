# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for TelemetryListenerDependencies parameter bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.listener.dependencies import TelemetryListenerDependencies
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListenerDependenciesTest(TestCase):
    '''
        Verifies TelemetryListenerDependencies initialization and immutability.
    '''

    def test_listener_dependencies_frozen(self) -> None:
        '''
            Verifies all collaborator ports, timeout_sec, and frozen guard.

            :exceptions: None.
        '''
        rx_port = Mock(spec=IByteReceiver)
        codec = Mock(spec=IBinaryCodec)
        inspector = Mock(spec=ITelemetryInspector)
        sink = Mock(spec=ITelemetrySink)
        clock = Mock(spec=IClock)
        controller = Mock(spec=ILoopController)
        stop_flag = Mock(spec=ISignalFlag)
        deps = TelemetryListenerDependencies(
            receiver=rx_port,
            codec=codec,
            inspector=inspector,
            sink=sink,
            clock=clock,
            controller=controller,
            stop_flag=stop_flag,
            timeout_sec=0.05,
        )
        self.assertIs(deps.receiver, rx_port)
        self.assertIs(deps.codec, codec)
        self.assertIs(deps.inspector, inspector)
        self.assertIs(deps.sink, sink)
        self.assertIs(deps.clock, clock)
        self.assertIs(deps.controller, controller)
        self.assertIs(deps.stop_flag, stop_flag)
        self.assertEqual(deps.timeout_sec, 0.05)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'timeout_sec', 0.2)


if __name__ == '__main__':
    main()
