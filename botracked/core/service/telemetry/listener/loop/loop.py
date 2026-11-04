# -*- coding: UTF-8 -*-

'''
Module
    loop.py
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
    Defines TelemetryListenerLoop consuming buffered RX chunks for decoding.
'''

from __future__ import annotations

from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.listener.decoder.idecoder import ITelemetryDecoder

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListenerLoop:
    '''
        Defines class TelemetryListenerLoop implementing ITelemetryListenerLoop
        and IRunnableWorker contracts structurally.
        Reads buffered chunks from IByteReceiver and forwards to ITelemetryDecoder.

        It defines:

            :attributes:
                | _receiver - Buffered inbound byte receiver port.
                | _decoder - Telemetry frame stream decoder port.
                | _stop_flag - Signal flag notifying loop termination.
                | _timeout_sec - Dequeue wait timeout duration in seconds.
            :methods:
                | __init__ - Initializes listener loop with injected ports.
                | run - Consumes buffered RX chunks until stop flag is set.
                | is_stopped - Checks if loop stop signal is active.
    '''

    _receiver: IByteReceiver
    _decoder: ITelemetryDecoder
    _stop_flag: ISignalFlag
    _timeout_sec: float

    def __init__(
        self,
        *,
        receiver: IByteReceiver,
        decoder: ITelemetryDecoder,
        stop_flag: ISignalFlag,
        timeout_sec: float,
    ) -> None:
        '''
            Initializes listener loop with injected collaborator ports.

            :param receiver: Buffered inbound byte receiver port.
            :param decoder: Telemetry frame stream decoder port.
            :param stop_flag: Signal flag notifying loop termination.
            :param timeout_sec: Dequeue wait timeout duration in seconds.
            :exceptions: None.
        '''
        self._receiver = receiver
        self._decoder = decoder
        self._stop_flag = stop_flag
        self._timeout_sec = timeout_sec

    def run(self) -> None:
        '''
            Consumes buffered RX byte chunks and decodes them until stopped.

            :exceptions: None.
        '''
        while not self._stop_flag.is_set():
            try:
                chunk: bytes = self._receiver.read_bytes(self._timeout_sec)
                self._decoder.decode_chunk(chunk)
            except QueueEmptyError:
                continue

    def is_stopped(self) -> bool:
        '''
            Checks if loop stop signal is active.

            :return: True if stop flag is set, False otherwise.
            :exceptions: None.
        '''
        return self._stop_flag.is_set()
