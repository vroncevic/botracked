# -*- coding: UTF-8 -*-

'''
Module
    iraw_io.py
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
    Defines structural protocol abstracting low-level serial byte I/O.
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
class IRawSerialIO(Protocol):
    '''
        Defines structural protocol for raw serial byte read, write, and flush.

        It defines:

            :methods:
                | read - Reads up to requested count of bytes from serial device.
                | write - Writes raw byte sequence to serial device.
                | flush - Flushes outgoing serial write buffer.
    '''

    def read(self, size: int) -> bytes:
        '''
            Reads up to requested count of bytes from serial device.

            :param size: Maximum number of bytes to read.
            :return: Read byte sequence.
        '''

    def write(self, data: bytes) -> int:
        '''
            Writes raw byte sequence to serial device.

            :param data: Byte sequence to write.
            :return: Number of bytes written.
        '''

    def flush(self) -> None:
        '''
            Flushes outgoing serial write buffer.
        '''
