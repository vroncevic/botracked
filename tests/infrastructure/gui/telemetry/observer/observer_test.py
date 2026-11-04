# -*- coding: UTF-8 -*-

'''
Module
    observer_test.py
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
    Unit tests for TelemetryObserver.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.telemetry.protocol.iobserver import ITelemetryObserver
from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.infrastructure.gui.telemetry.iview import ITelemetryView
from botracked.infrastructure.gui.telemetry.observer.observer import TelemetryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryObserverTest(TestCase):
    '''
        Tests TelemetryObserver thread-safe scheduling and packet counting.
    '''

    def test_telemetry_and_packet_scheduling(self) -> None:
        '''
            Verifies on_telemetry, on_packet, get_packet_count, and reset.

            :exceptions: None.
        '''
        sched = MagicMock(spec=Tk)
        view = MagicMock(spec=ITelemetryView)
        sink = MagicMock(spec=IPacketStreamSink)
        observer = TelemetryObserver(sched, view, sink)
        self.assertIsInstance(observer, ITelemetryObserver)

        sample = TelemetryData('NORMAL', MotionCommand.STOP, 0, 0, 100, 'STOP', 'STOP', 0.0, True)
        observer.on_telemetry(sample)
        sched.after.assert_called_once_with(0, view.update_telemetry, sample)

        observer.on_packet(PacketDirection.TX, 'PING', b'\xaa\x01')
        self.assertEqual(observer.get_packet_count(), 1)
        sched.after.assert_any_call(0, view.update_packet_count, 1)
        sched.after.assert_any_call(0, sink.append_packet, 'TX', 'PING', 'AA 01')

        observer.reset()
        self.assertEqual(observer.get_packet_count(), 0)
        sched.after.assert_any_call(0, view.reset_telemetry)

if __name__ == '__main__':
    main()
