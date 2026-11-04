# -*- coding: UTF-8 -*-

'''
Module
    control.py
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
    Provides RawSerialControl adapter implementing IRawSerialControl structurally.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str
from serial import Serial

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RawSerialControl:
    '''
        Defines class RawSerialControl implementing IRawSerialControl structurally.
        Encapsulates PySerial Serial device lifecycle and configuration.

        It defines:

            :attributes:
                | _serial - Underlying physical serial port primitive.
            :methods:
                | __init__ - Initializes RawSerialControl with serial instance.
                | open - Opens and configures physical serial device handle.
                | close - Closes physical serial device handle.
                | is_open - Checks whether physical serial device is open.
                | __str__ - Returns string representation of control adapter.
    '''

    _serial: Serial

    def __init__(self, serial: Serial) -> None:
        '''
            Initializes RawSerialControl with serial instance.

            :param serial: Underlying physical serial primitive.
            :exceptions: None.
        '''
        self._serial = serial

    def open(self, port_name: str, baudrate: int) -> bool:
        '''
            Opens and configures physical serial device handle.

            :param port_name: System serial port identifier.
            :param baudrate: Communication speed in bauds.
            :return: True if device opened successfully, False otherwise.
            :exceptions: None.
        '''
        if self._serial.is_open:
            self._serial.close()
        self._serial.port = port_name
        self._serial.baudrate = baudrate
        self._serial.open()
        return self._serial.is_open

    def close(self) -> None:
        '''
            Closes physical serial device handle.

            :exceptions: None.
        '''
        if self._serial.is_open:
            self._serial.close()

    def is_open(self) -> bool:
        '''
            Checks whether physical serial device is open.

            :return: True if open, False otherwise.
            :exceptions: None.
        '''
        return self._serial.is_open

    def __str__(self) -> str:
        '''
            Returns string representation of control adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
