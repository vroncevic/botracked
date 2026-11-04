# -*- coding: UTF-8 -*-

'''
Module
    iobserver.py
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
    Defines ITelemetryObserver structural protocol interface.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.telemetry_data import TelemetryData

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITelemetryObserver(Protocol):
    '''
        Defines protocol ITelemetryObserver with method(s).
        Structural interface for observing robot telemetry and packet activity.

        It defines:

            :methods:
                | on_telemetry - Handles decoded telemetry status update.
                | on_packet - Handles raw packet transmission or reception event.
    '''

    def on_telemetry(self, data: TelemetryData) -> None:
        '''
            Handles decoded telemetry status update.

            :param data: Decoded robot telemetry snapshot.
        '''

    def on_packet(
        self,
        direction: PacketDirection,
        description: str,
        raw_bytes: bytes,
    ) -> None:
        '''
            Handles raw packet transmission or reception event.

            :param direction: Transfer direction enumeration value.
            :param description: Human-readable frame description.
            :param raw_bytes: Raw packet binary content.
        '''
