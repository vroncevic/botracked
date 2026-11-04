# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Defines BotTelemetryService coordinating telemetry distribution.
'''

from __future__ import annotations

from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.telemetry.protocol.iobserver import ITelemetryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotTelemetryService:
    '''
        Defines class BotTelemetryService implementing IBotTelemetryService
        and ITelemetrySink structurally.
        Coordinates telemetry observer registrations and event fanout.

        It defines:

            :attributes:
                | _observers - Registered subscribers implementing ITelemetryObserver.
            :methods:
                | __init__ - Initializes empty telemetry observer registry.
                | add_observer - Registers an observer for telemetry and packets.
                | remove_observer - Unregisters a previously registered observer.
                | notify_telemetry - Broadcasts decoded telemetry update to observers.
                | notify_packet - Broadcasts raw packet trace event to observers.
    '''

    _observers: list[ITelemetryObserver]

    def __init__(self) -> None:
        '''
            Initializes empty telemetry observer registry.

            :exceptions: None.
        '''
        self._observers = []

    def add_observer(self, observer: ITelemetryObserver) -> None:
        '''
            Registers an observer for telemetry and packet notifications.

            :param observer: Subscriber instance.
            :exceptions: None.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: ITelemetryObserver) -> None:
        '''
            Unregisters a previously registered telemetry observer.

            :param observer: Subscriber instance to remove.
            :exceptions: None.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_telemetry(self, data: TelemetryData) -> None:
        '''
            Broadcasts decoded telemetry update to all registered observers.

            :param data: Decoded telemetry snapshot.
            :exceptions: None.
        '''
        for observer in tuple(self._observers):
            observer.on_telemetry(data)

    def notify_packet(
        self,
        direction: PacketDirection,
        description: str,
        raw_bytes: bytes,
    ) -> None:
        '''
            Broadcasts raw packet trace event to all registered observers.

            :param direction: Transfer direction enumeration value.
            :param description: Human-readable frame description.
            :param raw_bytes: Raw binary wire frame.
            :exceptions: None.
        '''
        for observer in tuple(self._observers):
            observer.on_packet(direction, description, raw_bytes)
