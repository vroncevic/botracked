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
    Defines reception worker task reading stream bytes into FIFO byte queue.
'''

from __future__ import annotations

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.service.connection.buffer.iqueue import IByteQueue
from botracked.core.service.connection.receiver.protocol.ireader import IByteReader

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReceptionTask:
    '''
        Defines class ReceptionTask implementing IByteReceiver and IWorkerTask
        contracts structurally.
        Reads raw byte chunks via IByteReader and buffers them in IByteQueue.

        It defines:

            :attributes:
                | _reader - Low-level hardware byte reader port.
                | _queue - Thread-safe FIFO inbound byte queue port.
                | _buffer_size - Maximum bytes requested per read iteration.
            :methods:
                | __init__ - Initializes reception task with reader, queue, size.
                | read_bytes - Dequeues next buffered inbound byte chunk.
                | has_pending - Checks whether inbound byte buffer holds chunks.
                | execute_step - Reads next chunk from stream and enqueues it.
                | cleanup - Cleans up task resources and flushes queue upon stopping.
    '''

    _reader: IByteReader
    _queue: IByteQueue
    _buffer_size: int

    def __init__(
        self,
        *,
        reader: IByteReader,
        queue: IByteQueue,
        buffer_size: int,
    ) -> None:
        '''
            Initializes reception task with reader, queue, and buffer size.

            :param reader: Low-level hardware byte reader port.
            :param queue: Thread-safe FIFO inbound byte queue port.
            :param buffer_size: Maximum bytes requested per read iteration.
            :exceptions: None.
        '''
        self._reader = reader
        self._queue = queue
        self._buffer_size = buffer_size

    def read_bytes(self, timeout: float) -> bytes:
        '''
            Dequeues next buffered inbound byte chunk.

            :param timeout: Maximum wait duration in seconds.
            :return: Dequeued byte sequence.
            :exceptions:
                | QueueEmptyError: If queue wait exceeds timeout.
        '''
        return self._queue.dequeue(timeout)

    def has_pending(self) -> bool:
        '''
            Checks whether inbound byte buffer holds unread byte chunks.

            :return: True if buffer is non-empty, False otherwise.
            :exceptions: None.
        '''
        return not self._queue.is_empty()

    def execute_step(self) -> bool:
        '''
            Reads next chunk from stream and enqueues into FIFO buffer.

            :return: True if reception should continue, False on error.
            :exceptions: None.
        '''
        try:
            data: bytes = self._reader.read_bytes(self._buffer_size)
        except BotConnectionError:
            return False

        if data:
            self._queue.enqueue(data)

        return True

    def cleanup(self) -> None:
        '''
            Cleans up task resources and flushes queue upon stopping.

            :exceptions: None.
        '''
        self._queue.clear()
