# -*- coding: UTF-8 -*-

'''
Module
    byte_queue.py
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
    Provides ByteQueue adapter implementing IByteQueue contract structurally.
'''

from __future__ import annotations

from queue import Empty

from ats_utilities.utils.reflection import to_str

from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.infrastructure.connection.buffer.iraw_queue import IRawByteQueue

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ByteQueue:
    '''
        Defines class ByteQueue implementing IByteQueue contract structurally.
        Adapts low-level thread-safe FIFO primitive without exposing queue exceptions.

        It defines:

            :attributes:
                | _raw_queue - Underlying thread-safe FIFO primitive port.
            :methods:
                | __init__ - Initializes ByteQueue with injected raw queue port.
                | enqueue - Appends byte sequence to outgoing FIFO buffer.
                | dequeue - Retrieves next byte sequence from buffer.
                | clear - Drains all buffered byte sequences from queue.
                | is_empty - Checks whether queue contains zero pending items.
                | __str__ - Returns string representation of adapter.
    '''

    _raw_queue: IRawByteQueue

    def __init__(self, raw_queue: IRawByteQueue) -> None:
        '''
            Initializes ByteQueue with injected raw queue port.

            :param raw_queue: Thread-safe FIFO primitive satisfying IRawByteQueue.
            :exceptions: None.
        '''
        self._raw_queue = raw_queue

    def enqueue(self, data: bytes) -> None:
        '''
            Appends byte sequence to outgoing FIFO buffer.

            :param data: Raw byte sequence to buffer.
            :exceptions: None.
        '''
        self._raw_queue.put(data)

    def dequeue(self, timeout: float) -> bytes:
        '''
            Retrieves next byte sequence from buffer.

            :param timeout: Maximum wait duration in seconds.
            :return: Dequeued byte sequence.
            :exceptions:
                | QueueEmptyError: If queue wait exceeds timeout.
        '''
        try:
            return self._raw_queue.get(True, timeout)

        except Empty as err:
            raise QueueEmptyError('Queue timed out waiting for byte data.') from err

    def clear(self) -> None:
        '''
            Drains all buffered byte sequences from queue.

            :exceptions: None.
        '''
        while not self._raw_queue.empty():
            try:
                self._raw_queue.get_nowait()

            except Empty:
                break

    def is_empty(self) -> bool:
        '''
            Checks whether queue contains zero pending items.

            :return: True if queue is empty, False otherwise.
            :exceptions: None.
        '''
        return self._raw_queue.empty()

    def __str__(self) -> str:
        '''
            Returns string representation of adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
