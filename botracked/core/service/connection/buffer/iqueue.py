# -*- coding: UTF-8 -*-

'''
Module
    iqueue.py
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
    Defines driven port IByteQueue for thread-safe FIFO byte buffering.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IByteQueue(Protocol):
    '''
        Defines driven port IByteQueue abstracting thread-safe FIFO byte buffering.

        It defines:

            :methods:
                | enqueue - Appends byte sequence to FIFO buffer.
                | dequeue - Retrieves next byte sequence from buffer.
                | clear - Drains all buffered byte sequences from queue.
                | is_empty - Checks whether queue contains zero pending items.
    '''

    def enqueue(self, data: bytes) -> None:
        '''
            Appends byte sequence to FIFO buffer.

            :param data: Raw byte sequence to buffer.
        '''

    def dequeue(self, timeout: float) -> bytes:
        '''
            Retrieves next byte sequence from buffer.

            :param timeout: Maximum wait duration in seconds.
            :return: Dequeued byte sequence.
        '''

    def clear(self) -> None:
        '''
            Drains all buffered byte sequences from queue.
        '''

    def is_empty(self) -> bool:
        '''
            Checks whether queue contains zero pending items.

            :return: True if queue is empty, False otherwise.
        '''
