# -*- coding: UTF-8 -*-

'''
Module
    task.py
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
    Defines transmission worker task draining FIFO byte queue onto stream writer.
'''

from __future__ import annotations

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.transmitter.protocol.iwriter import IByteWriter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmissionTask:
    '''
        Defines class TransmissionTask implementing IByteTransmitter and
        IWorkerTask contracts structurally.
        Buffers outbound chunks in IByteQueue and writes them via IByteWriter.

        It defines:

            :attributes:
                | _writer - Low-level hardware byte writer port.
                | _queue - Thread-safe FIFO outbound byte queue port.
                | _timeout - Maximum seconds to wait for next item in queue.
            :methods:
                | __init__ - Initializes transmission task with writer, queue, timeout.
                | write_bytes - Enqueues raw bytes into outbound FIFO buffer.
                | has_pending - Checks whether outbound byte buffer holds chunks.
                | execute_step - Dequeues and writes next available chunk.
                | cleanup - Cleans up task resources and flushes queue upon stopping.
    '''

    _writer: IByteWriter
    _queue: IByteQueue
    _timeout: float

    def __init__(
        self,
        *,
        writer: IByteWriter,
        queue: IByteQueue,
        timeout: float,
    ) -> None:
        '''
            Initializes transmission task with writer, queue, and timeout.

            :param writer: Low-level hardware byte writer port.
            :param queue: Thread-safe FIFO outbound byte queue port.
            :param timeout: Maximum seconds to wait for next queued item.
            :exceptions: None.
        '''
        self._writer = writer
        self._queue = queue
        self._timeout = timeout

    def write_bytes(self, data: bytes) -> bool:
        '''
            Transmits raw bytes asynchronously by enqueuing into FIFO buffer.

            :param data: Byte sequence to write.
            :return: True if successfully enqueued, False otherwise.
            :exceptions: None.
        '''
        self._queue.enqueue(data)
        return True

    def has_pending(self) -> bool:
        '''
            Checks whether outbound byte buffer holds unsent byte chunks.

            :return: True if buffer is non-empty, False otherwise.
            :exceptions: None.
        '''
        return not self._queue.is_empty()

    def execute_step(self) -> bool:
        '''
            Dequeues and transmits next available chunk.

            :return: True if transmission should continue, False on error.
            :exceptions: None.
        '''
        try:
            payload: bytes = self._queue.dequeue(self._timeout)
            return self._writer.write_bytes(payload)
        except QueueEmptyError:
            return True
        except BotConnectionError:
            return False

    def cleanup(self) -> None:
        '''
            Cleans up task resources and flushes queue upon stopping.

            :exceptions: None.
        '''
        self._queue.clear()
