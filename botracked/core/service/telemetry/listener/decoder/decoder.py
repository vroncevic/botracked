# -*- coding: UTF-8 -*-

'''
Module
    decoder.py
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
    Defines TelemetryDecoder extracting protocol frames and telemetry snapshots.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryDecoder:
    '''
        Defines class TelemetryDecoder implementing ITelemetryDecoder structurally.
        Decodes incoming byte chunks into protocol frames and broadcasts telemetry.

        It defines:

            :attributes:
                | MS_PER_SECOND - Milliseconds per second conversion factor.
                | _codec - Binary frame stream decoder.
                | _inspector - Telemetry payload field decoder.
                | _sink - Narrow sink broadcasting telemetry and packet events.
                | _clock - Monotonic clock port computing connection uptime.
                | _start_time - Monotonic timestamp marking start of session.
            :methods:
                | __init__ - Initializes telemetry decoder with collaborators.
                | reset_session - Resets framing buffer and restarts session clock.
                | decode_chunk - Decodes raw byte chunk and distributes updates.
                | process_frame - Publishes packet trace and decoded telemetry.
    '''

    MS_PER_SECOND: ClassVar[int] = 1000

    _codec: IBinaryCodec
    _inspector: ITelemetryInspector
    _sink: ITelemetrySink
    _clock: IClock
    _start_time: float

    def __init__(
        self,
        *,
        codec: IBinaryCodec,
        inspector: ITelemetryInspector,
        sink: ITelemetrySink,
        clock: IClock,
    ) -> None:
        '''
            Initializes telemetry decoder with codec, inspector, sink, and clock.

            :param codec: Binary frame stream decoder.
            :param inspector: Telemetry payload field decoder.
            :param sink: Narrow sink publishing telemetry and packet trace events.
            :param clock: Monotonic clock port computing elapsed uptime.
            :exceptions: None.
        '''
        self._codec = codec
        self._inspector = inspector
        self._sink = sink
        self._clock = clock
        self._start_time = clock.monotonic()

    def reset_session(self) -> None:
        '''
            Resets binary stream framing buffer and restarts session uptime clock.

            :exceptions: None.
        '''
        self._codec.reset()
        self._start_time = self._clock.monotonic()

    def decode_chunk(self, data: bytes) -> None:
        '''
            Decodes raw byte chunk into frames and broadcasts updates to sink.

            :param data: Inbound bytes payload.
            :exceptions: None.
        '''
        for opcode, payload in self._codec.decode_stream(data):
            self.process_frame(opcode, payload)

    def process_frame(self, opcode: int, payload: bytes) -> None:
        '''
            Publishes packet trace and decoded status telemetry for a wire frame.

            :param opcode: Decoded protocol frame opcode integer.
            :param payload: Decoded protocol frame payload bytes.
            :exceptions: None.
        '''
        try:
            op_name: str = ProtocolOpcode(opcode).name
        except ValueError:
            op_name = f'0x{opcode:02X}'

        self._sink.notify_packet(PacketDirection.RX, op_name, payload)

        if opcode in (ProtocolOpcode.RESP_STATUS, ProtocolOpcode.RESP_DIAG):
            uptime: int = int(
                (self._clock.monotonic() - self._start_time) * self.MS_PER_SECOND
            )
            snapshot = self._inspector.decode_payload(
                payload,
                is_connected=True,
                uptime_ms=uptime,
            )
            self._sink.notify_telemetry(snapshot)
