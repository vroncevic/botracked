# -*- coding: UTF-8 -*-

'''
Module
    idriver.py
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
    Defines structural interface ISerialDriver for synchronized serial access.
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
class ISerialDriver(Protocol):
    '''
        Defines structural interface ISerialDriver for synchronized serial access.

        It defines:

            :methods:
                | open_port - Configures and opens physical serial port.
                | close_port - Closes active physical serial port.
                | is_open - Checks whether serial port is currently open.
                | read_chunk - Reads raw byte chunk from open serial port.
                | write_chunk - Writes and flushes raw byte chunk.
    '''

    def open_port(self, port_name: str, baudrate: int) -> bool:
        '''
            Configures and opens physical serial port.

            :param port_name: System serial port identifier.
            :param baudrate: Communication speed in bauds.
            :return: True if port opened successfully, False otherwise.
        '''

    def close_port(self) -> None:
        '''
            Closes active physical serial port.
        '''

    def is_open(self) -> bool:
        '''
            Checks whether serial port is currently open.

            :return: True if open, False otherwise.
        '''

    def read_chunk(self, max_size: int) -> bytes:
        '''
            Reads raw byte chunk from open serial port.

            :param max_size: Maximum number of bytes to read.
            :return: Received byte sequence.
        '''

    def write_chunk(self, data: bytes) -> int:
        '''
            Writes and flushes raw byte chunk.

            :param data: Raw byte sequence to transmit.
            :return: Number of bytes written.
        '''
