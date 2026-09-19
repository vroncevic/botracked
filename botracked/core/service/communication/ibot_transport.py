# -*- coding: UTF-8 -*-

'''
Module
    ibot_transport.py
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
    Defines IBotTransport interface for physical and network communication channels.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBotTransport(Protocol):
    '''
        Defines protocol IBotTransport with method(s).
        Protocol representing low-level byte stream transport (Serial / TCP).

        It defines:

            :methods:
                | connect - Establishes communication with robot according to params.
                | disconnect - Closes active connection and releases OS handles.
                | is_connected - Checks if transport is currently connected.
                | send - Transmits raw bytes over active channel.
                | receive - Reads available incoming bytes from the channel.
    '''

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Establishes communication with robot according to params.

            :param params: Connection parameters (port, baud, IP, etc.).
            :return: True if connected successfully, False otherwise.
        '''

    def disconnect(self) -> None:
        '''
            Closes active connection and releases OS handles.
        '''

    def is_connected(self) -> bool:
        '''
            Checks if transport is currently connected and healthy.

            :return: True if connected, False otherwise.
        '''

    def send(self, data: bytes) -> bool:
        '''
            Transmits raw bytes over active channel.

            :param data: Byte sequence to transmit.
            :return: True if sent successfully, False otherwise.
        '''

    def receive(self, max_bytes: int = 1024) -> bytes:
        '''
            Reads available incoming bytes from the channel.

            :param max_bytes: Maximum byte count to read.
            :return: Raw bytes received, or empty bytes if nothing available.
        '''
