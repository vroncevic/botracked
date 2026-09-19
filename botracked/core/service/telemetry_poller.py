# -*- coding: UTF-8 -*-

'''
Module
    telemetry_poller.py
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
    Provides TelemetryPoller background thread for continuous telemetry streaming.
'''

from __future__ import annotations

from collections.abc import Callable
from threading import Event, Thread
from time import sleep, time

from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.communication.binary_codec import BinaryCodec
from botracked.infrastructure.communication.serial_transport import SerialTransport
from botracked.infrastructure.communication.tcp_transport import TcpTransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPoller:
    '''
        Defines class TelemetryPoller with attribute(s) and method(s).
        Background worker receiving and decoding robot telemetry packets.

        It defines:

            :attributes:
                | _stop_event - Cancellation event flag for stopping worker thread.
                | _thread - Worker thread instance or None.
                | _codec - Binary frame codec for stream decoding.
                | _on_telemetry - Callback for parsed telemetry data notifications.
                | _on_packet - Callback for packet logging notifications.
                | _request_status_fn - Callback querying telemetry status periodically.
                | _start_time - Timestamp when polling commenced.
            :methods:
                | __init__ - Initializes poller with codec and notification callbacks.
                | start - Starts the background polling thread.
                | stop - Stops the background polling thread.
                | _worker - Background worker loop reading frames and polling status.
    '''

    _stop_event: Event
    _thread: Thread | None
    _codec: BinaryCodec
    _on_telemetry: Callable[[TelemetryData], None]
    _on_packet: Callable[[str, str, str], None]
    _request_status_fn: Callable[[], bool]
    _start_time: float

    def __init__(
        self,
        codec: BinaryCodec,
        on_telemetry: Callable[[TelemetryData], None],
        on_packet: Callable[[str, str, str], None],
        request_status_fn: Callable[[], bool],
    ) -> None:
        '''
            Initializes poller with codec and notification callbacks.

            :param codec: Binary frame codec.
            :param on_telemetry: Telemetry notification callback.
            :param on_packet: Raw packet notification callback.
            :param request_status_fn: Callback requesting status frame.
            :exceptions: None.
        '''
        self._stop_event = Event()
        self._thread = None
        self._codec = codec
        self._on_telemetry = on_telemetry
        self._on_packet = on_packet
        self._request_status_fn = request_status_fn
        self._start_time = 0.0

    def start(self, transport: SerialTransport | TcpTransport) -> None:
        '''
            Starts the background polling thread.

            :param transport: Active connected transport instance.
            :exceptions: None.
        '''
        self.stop()
        self._stop_event.clear()
        self._start_time = time()
        self._thread = Thread(target=self._worker, args=(transport,), daemon=True)
        self._thread.start()

    def stop(self) -> None:
        '''
            Stops the background polling thread.

            :exceptions: None.
        '''
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=0.2)
        self._thread = None

    def _worker(self, transport: SerialTransport | TcpTransport) -> None:
        '''
            Background worker loop reading incoming bytes and querying status.

            :param transport: Active connected transport instance.
            :exceptions: None.
        '''
        poll_ticks: int = 0

        while not self._stop_event.is_set() and transport.is_connected():
            chunk: bytes = transport.receive(512)

            if chunk:
                frames = self._codec.decode_stream(chunk)

                for opcode, payload in frames:
                    try:
                        op_name: str = ProtocolOpcode(opcode).name

                    except ValueError:
                        op_name = f'0x{opcode:02X}'

                    wire: str = (
                        bytes([0xAA, opcode, len(payload)]).hex().upper()
                        + payload.hex().upper()
                    )
                    self._on_packet('RX', op_name, wire)

                    if opcode in (
                        ProtocolOpcode.RESP_STATUS,
                        ProtocolOpcode.RESP_DIAG,
                    ):
                        uptime_ms: int = int((time() - self._start_time) * 1000)
                        telemetry: TelemetryData = (
                            TelemetryData.from_status_payload(
                                payload,
                                is_connected=True,
                                uptime_ms=uptime_ms,
                            )
                        )
                        self._on_telemetry(telemetry)

            poll_ticks += 1

            if poll_ticks >= 10:
                poll_ticks = 0
                self._request_status_fn()

            sleep(0.05)
