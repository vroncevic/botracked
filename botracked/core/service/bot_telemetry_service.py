# -*- coding: UTF-8 -*-

'''
Module
    bot_telemetry_service.py
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
    Provides BotTelemetryService managing subscribers, telemetry snapshots, and packet logs.
'''

from __future__ import annotations

from collections.abc import Callable

from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.communication.binary_codec import (
    BinaryCodec,
)
from botracked.infrastructure.communication.serial_transport import (
    SerialTransport,
)
from botracked.infrastructure.communication.tcp_transport import (
    TcpTransport,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotTelemetryService:
    '''
        Defines class BotTelemetryService with attribute(s) and method(s).
        Coordinator for telemetry notifications, incoming packet dispatch, and polling.

        It defines:

            :attributes:
                | _codec - Binary frame encoder/decoder.
                | _transport_provider - Supplier for currently active transport.
                | _telemetry - Current TelemetryData snapshot.
                | _observers - Registered observer instances.
            :methods:
                | __init__ - Initializes telemetry service.
                | add_observer - Registers an observer for telemetry and packet events.
                | remove_observer - Unregisters an observer.
                | notify_connection_state - Broadcasts connection state transition.
                | notify_telemetry - Broadcasts telemetry update to observers.
                | notify_packet - Broadcasts raw packet event to observers.
                | request_status - Queries telemetry status frame from robot.
                | get_telemetry - Returns most recent telemetry snapshot.
    '''

    _codec: BinaryCodec
    _transport_provider: Callable[[], SerialTransport | TcpTransport | None]
    _telemetry: TelemetryData
    _observers: list[object]

    def __init__(
        self,
        codec: BinaryCodec,
        transport_provider: Callable[[], SerialTransport | TcpTransport | None],
    ) -> None:
        '''
            Initializes telemetry service.

            :param codec: Binary frame encoder/decoder.
            :param transport_provider: Supplier for currently active transport.
            :exceptions: None.
        '''
        self._codec = codec
        self._transport_provider = transport_provider
        self._telemetry = TelemetryData.default_offline()
        self._observers = []

    def add_observer(self, observer: object) -> None:
        '''
            Registers an observer for telemetry and packet notifications.

            :param observer: Subscriber instance.
            :exceptions: None.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: object) -> None:
        '''
            Unregisters an observer.

            :param observer: Subscriber instance.
            :exceptions: None.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_connection_state(self, is_connected: bool, message: str) -> None:
        '''
            Broadcasts connection state transition to observers.

            :param is_connected: True if link is up, False otherwise.
            :param message: Diagnostic description.
            :exceptions: None.
        '''
        for observer in list(self._observers):
            if hasattr(observer, 'on_connection_state_changed'):
                getattr(observer, 'on_connection_state_changed')(
                    is_connected, message
                )

    def notify_telemetry(self, data: TelemetryData) -> None:
        '''
            Broadcasts telemetry update to observers.

            :param data: Fresh TelemetryData instance.
            :exceptions: None.
        '''
        self._telemetry = data
        for observer in list(self._observers):
            if hasattr(observer, 'on_telemetry_updated'):
                getattr(observer, 'on_telemetry_updated')(data)
            elif hasattr(observer, 'on_telemetry'):
                getattr(observer, 'on_telemetry')(data)

    def notify_packet(self, tx_rx: str, name: str, raw: bytes | str) -> None:
        '''
            Broadcasts raw packet event to observers.

            :param tx_rx: Transmission direction indicator (TX or RX).
            :param name: Packet description.
            :param raw: Hex bytes or string representation.
            :exceptions: None.
        '''
        hex_str: str = raw.hex().upper() if isinstance(raw, bytes) else str(raw)
        for observer in list(self._observers):
            if hasattr(observer, 'on_packet_logged'):
                getattr(observer, 'on_packet_logged')(tx_rx, name, hex_str)
            elif hasattr(observer, 'on_packet'):
                getattr(observer, 'on_packet')(tx_rx, name, raw)

    def request_status(self) -> bool:
        '''
            Queries telemetry status frame from robot.

            :return: True if request sent, False otherwise.
            :exceptions: None.
        '''
        transport = self._transport_provider()
        if transport is None or not transport.is_connected():
            return False
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_GET_STATUS)
        sent = transport.send(frame)
        if sent:
            self.notify_packet('TX', 'CMD_GET_STATUS', frame)
        return sent

    def get_telemetry(self) -> TelemetryData:
        '''
            Returns most recent telemetry snapshot.

            :return: Current TelemetryData.
            :exceptions: None.
        '''
        return self._telemetry
