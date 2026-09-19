# -*- coding: UTF-8 -*-

'''
Module
    connection_params.py
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
    Defines ConnectionParams value object holding transport configuration.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ConnectionParams:
    '''
        Immutable parameters for establishing communication with tracked_bot.

        It defines:

            :attributes:
                | connection_type - Connection protocol identifier ('SERIAL' or 'TCP').
                | serial_port - Filesystem path to hardware serial device.
                | baud_rate - Communication transmission speed in baud.
                | tcp_host - IP address or hostname of wireless network endpoint.
                | tcp_port - TCP port number of network listener.
                | timeout - Socket or serial link timeout duration in seconds.
            :methods:
                | is_serial - Checks if connection mode is serial.
                | is_tcp - Checks if connection mode is TCP socket.
                | description - Returns human-readable description of endpoint.
    '''

    connection_type: str = 'SERIAL'
    serial_port: str = '/dev/ttyUSB0'
    baud_rate: int = 115200
    tcp_host: str = '192.168.4.1'
    tcp_port: int = 8888
    timeout: float = 1.0

    @property
    def is_serial(self) -> bool:
        '''
            Checks if connection mode is serial.

            :return: True if serial, False otherwise.
            :exceptions: None.
        '''
        return self.connection_type.upper() == 'SERIAL'

    @property
    def is_tcp(self) -> bool:
        '''
            Checks if connection mode is TCP socket.

            :return: True if TCP, False otherwise.
            :exceptions: None.
        '''
        return self.connection_type.upper() == 'TCP'

    @property
    def description(self) -> str:
        '''
            Returns human-readable description of endpoint.

            :return: Endpoint description string.
            :exceptions: None.
        '''
        if self.is_serial:
            return f'Serial({self.serial_port} @ {self.baud_rate} baud)'
        return f'TCP({self.tcp_host}:{self.tcp_port})'
