# -*- coding: UTF-8 -*-

'''
Module
    iraw_queue.py
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
    Defines structural protocol IRawByteQueue wrapping low-level FIFO queue primitives.
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
class IRawByteQueue(Protocol):
    '''
        Defines structural contract IRawByteQueue for thread-safe FIFO primitives.

        It defines:

            :methods:
                | put - Enqueues raw byte item into underlying FIFO storage.
                | get - Dequeues raw byte item blocking up to timeout.
                | get_nowait - Dequeues raw byte item without blocking.
                | empty - Checks whether underlying FIFO storage is empty.
    '''

    def put(self, item: bytes) -> None:
        '''
            Enqueues raw byte item into underlying FIFO storage.

            :param item: Raw byte sequence to enqueue.
        '''

    def get(self, block: bool, timeout: float) -> bytes:
        '''
            Dequeues raw byte item blocking up to timeout.

            :param block: True to block until item or timeout.
            :param timeout: Maximum wait duration in seconds.
            :return: Dequeued byte sequence.
        '''

    def get_nowait(self) -> bytes:
        '''
            Dequeues raw byte item without blocking.

            :return: Dequeued byte sequence.
        '''

    def empty(self) -> bool:
        '''
            Checks whether underlying FIFO storage is empty.

            :return: True if storage is empty, False otherwise.
        '''
