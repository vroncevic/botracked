# -*- coding: UTF-8 -*-

'''
Module
    serial.py
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
    Defines SerialReceiver reading raw stream byte sequences via serial driver.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str
from serial import SerialException

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.receiver_error import ReceiverError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialReceiver:
    '''
        Defines class SerialReceiver implementing IByteReader structurally.
        Reads incoming bytes from synchronized serial driver port.

        It defines:

            :attributes:
                | _driver - Synchronized low-level serial driver port.
            :methods:
                | __init__ - Initializes serial receiver with driver port.
                | is_open - Checks whether underlying serial driver is open.
                | read_bytes - Reads raw byte payload from communication stream.
                | __str__ - Returns string representation of adapter.
    '''

    _driver: ISerialDriver

    def __init__(self, driver: ISerialDriver) -> None:
        '''
            Initializes serial receiver with synchronized driver port.

            :param driver: Synchronized low-level serial driver port.
            :exceptions: None.
        '''
        self._driver = driver

    def is_open(self) -> bool:
        '''
            Checks whether underlying serial driver stream is open.

            :return: True if driver port is open, False otherwise.
            :exceptions: None.
        '''
        return self._driver.is_open()

    def read_bytes(self, size: int) -> bytes:
        '''
            Reads raw byte payload from communication stream.

            :param size: Maximum number of bytes to read.
            :return: Received byte payload.
            :exceptions:
                | PortDisconnectedError: If serial port is not connected.
                | ReceiverError: If serial read fails.
        '''
        if not self.is_open():
            raise PortDisconnectedError('Serial port is not connected.')

        try:
            return self._driver.read_chunk(size)

        except (SerialException, OSError) as err:
            raise ReceiverError(f'Serial read error: {err}') from err

    def __str__(self) -> str:
        '''
            Returns string representation of SerialReceiver adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
