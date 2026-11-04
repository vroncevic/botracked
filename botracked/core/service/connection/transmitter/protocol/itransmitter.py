# -*- coding: UTF-8 -*-

'''
Module
    itransmitter.py
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
    Defines structural interface IByteTransmitter for buffered byte transmission.
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
class IByteTransmitter(Protocol):
    '''
        Defines structural protocol for enqueuing outbound raw byte chunks.

        It defines:

            :methods:
                | write_bytes - Enqueues raw bytes for asynchronous transmission.
                | has_pending - Checks whether outbound byte buffer holds chunks.
    '''

    def write_bytes(self, data: bytes) -> bool:
        '''
            Enqueues raw bytes for asynchronous transmission over communication link.

            :param data: Byte sequence to transmit.
            :return: True if bytes queued for transmission, False otherwise.
        '''

    def has_pending(self) -> bool:
        '''
            Checks whether outbound byte buffer holds unsent byte chunks.

            :return: True if buffer is non-empty, False otherwise.
        '''
