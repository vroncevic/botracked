# -*- coding: UTF-8 -*-

'''
Module
    observer.py
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
    Defines TelemetryObserver bridging background observer events to UI.
'''

from __future__ import annotations

from tkinter import Tk
from typing import ClassVar

from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.infrastructure.gui.telemetry.iview import ITelemetryView

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryObserver:
    '''
        Defines class TelemetryObserver implementing ITelemetryObserver
        contract structurally without loose lambdas.

        It defines:

            :attributes:
                | IMMEDIATE_MS - Zero-delay UI thread dispatch constant.
                | HEX_SEP - Byte separator for formatted wire hex dumps.
                | _scheduler - Main-thread UI root window scheduler.
                | _view - Telemetry view receiving thread-safe updates.
                | _packet_sink - Console packet stream sink receiving traces.
                | _packet_count - Total observed raw packets.
            :methods:
                | __init__ - Initializes observer with scheduler, view, and sink.
                | on_telemetry - Handles decoded telemetry status update.
                | on_packet - Updates packet counter and forwards hex trace.
                | get_packet_count - Returns observed packet count.
                | reset - Resets telemetry view and packet counter.
    '''

    IMMEDIATE_MS: ClassVar[int] = 0
    HEX_SEP: ClassVar[str] = ' '

    _scheduler: Tk
    _view: ITelemetryView
    _packet_sink: IPacketStreamSink
    _packet_count: int

    def __init__(
        self,
        scheduler: Tk,
        view: ITelemetryView,
        packet_sink: IPacketStreamSink,
    ) -> None:
        '''
            Initializes observer with UI scheduler, telemetry view, and sink.

            :param scheduler: Main-thread UI root window scheduler.
            :param view: Target ITelemetryView receiving safe updates.
            :param packet_sink: Target IPacketStreamSink receiving wire traces.
            :exceptions: None.
        '''
        self._scheduler = scheduler
        self._view = view
        self._packet_sink = packet_sink
        self._packet_count = 0

    def on_telemetry(self, data: TelemetryData) -> None:
        '''
            Handles decoded telemetry status update safely across threads.

            :param data: Decoded robot telemetry snapshot.
            :exceptions: None.
        '''
        self._scheduler.after(
            self.IMMEDIATE_MS, self._view.update_telemetry, data
        )

    def on_packet(
        self,
        direction: PacketDirection,
        description: str,
        raw_bytes: bytes,
    ) -> None:
        '''
            Updates packet counter and streams formatted hex frame to console.

            :param direction: Transfer direction enumeration value.
            :param description: Human-readable frame description.
            :param raw_bytes: Raw packet binary content.
            :exceptions: None.
        '''
        self._packet_count += 1
        cnt: int = self._packet_count
        raw_hex: str = raw_bytes.hex(self.HEX_SEP).upper()
        self._scheduler.after(
            self.IMMEDIATE_MS, self._view.update_packet_count, cnt
        )
        self._scheduler.after(
            self.IMMEDIATE_MS,
            self._packet_sink.append_packet,
            str(direction),
            description,
            raw_hex,
        )

    def get_packet_count(self) -> int:
        '''
            Returns observed packet count.

            :return: Integer packet count.
            :exceptions: None.
        '''
        return self._packet_count

    def reset(self) -> None:
        '''
            Resets telemetry view and packet counter.

            :exceptions: None.
        '''
        self._packet_count = 0
        self._scheduler.after(
            self.IMMEDIATE_MS, self._view.reset_telemetry
        )
