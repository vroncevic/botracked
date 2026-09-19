# -*- coding: UTF-8 -*-

'''
Module
    itelemetry_observer.py
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
    Defines ITelemetryObserver interface for event notifications to subscribers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.telemetry_data import TelemetryData

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITelemetryObserver(Protocol):
    '''
        Defines protocol ITelemetryObserver with method(s).
        Observer interface for listening to telemetry events, connection state,
        and packet traffic.

        It defines:

            :methods:
                | on_telemetry_updated - Invoked when a new telemetry packet is decoded.
                | on_connection_state_changed - Invoked on connection change.
                | on_packet_logged - Invoked when a frame is sent or received.
    '''

    def on_telemetry_updated(self, telemetry: TelemetryData) -> None:
        '''
            Invoked when a new valid status/telemetry packet is decoded.

            :param telemetry: Updated TelemetryData snapshot.
        '''

    def on_connection_state_changed(
        self, is_connected: bool, message: str
    ) -> None:
        '''
            Invoked when transport connects or disconnects.

            :param is_connected: True if connected, False if disconnected.
            :param message: Informational or error description.
        '''

    def on_packet_logged(
        self, direction: str, opcode_name: str, raw_hex: str
    ) -> None:
        '''
            Invoked when a frame is sent (TX) or received (RX) for stream logging.

            :param direction: Direction indicator (TX or RX).
            :param opcode_name: Friendly opcode label.
            :param raw_hex: Hexadecimal string representation of packet.
        '''
