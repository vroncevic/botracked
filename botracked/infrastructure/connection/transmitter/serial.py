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
    Defines SerialTransmitter sending raw stream byte sequences via serial driver.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str
from serial import SerialException

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.transmitter_error import TransmitterError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransmitter:
    '''
        Defines class SerialTransmitter implementing IByteWriter structurally.
        Transmits outgoing bytes via synchronized serial driver port.

        It defines:

            :attributes:
                | _driver - Synchronized low-level serial driver port.
            :methods:
                | __init__ - Initializes serial transmitter with driver port.
                | is_open - Checks whether underlying serial driver is open.
                | write_bytes - Transmits raw bytes over communication interface.
                | __str__ - Returns string representation of adapter.
    '''

    _driver: ISerialDriver

    def __init__(self, driver: ISerialDriver) -> None:
        '''
            Initializes serial transmitter with synchronized driver port.

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

    def write_bytes(self, data: bytes) -> bool:
        '''
            Transmits raw bytes over communication interface.

            :param data: Byte sequence to write.
            :return: True if all bytes written, False otherwise.
            :exceptions:
                | PortDisconnectedError: If serial port is not connected.
                | TransmitterError: If serial write fails.
        '''
        if not self.is_open():
            raise PortDisconnectedError('Serial port is not connected.')

        try:
            written: int = self._driver.write_chunk(data)
            return written == len(data)

        except (SerialException, OSError) as err:
            raise TransmitterError(f'Serial write error: {err}') from err

    def __str__(self) -> str:
        '''
            Returns string representation of SerialTransmitter adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
