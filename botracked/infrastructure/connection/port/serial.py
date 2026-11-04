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
    Defines SerialPort adapter managing hardware connection lifecycle via driver.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str
from serial import SerialException

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPort:
    '''
        Defines class SerialPort implementing IConnectionPort and IConnectionStatus.
        Delegates hardware serial port lifecycle to injected ISerialDriver port.

        It defines:

            :attributes:
                | _driver - Synchronized serial driver interface.
            :methods:
                | __init__ - Initializes serial port adapter with driver port.
                | connect - Establishes communication port connection.
                | disconnect - Terminates active port connection.
                | is_connected - Checks if communication port is open.
                | get_version - Returns component semantic version string.
                | __str__ - Returns string representation of adapter.
    '''

    _driver: ISerialDriver

    def __init__(self, driver: ISerialDriver) -> None:
        '''
            Initializes serial port adapter with synchronized driver port.

            :param driver: Synchronized serial driver interface.
            :exceptions: None.
        '''
        self._driver = driver

    def connect(self, port_name: str, baudrate: int) -> bool:
        '''
            Establishes communication port connection.

            :param port_name: System port identifier.
            :param baudrate: Communication speed in bauds.
            :return: True if connected successfully, False otherwise.
            :exceptions:
                | BotConnectionError: If serial port failed to open.
        '''
        try:
            return self._driver.open_port(port_name, baudrate)
        except (SerialException, OSError) as err:
            raise BotConnectionError(f'Failed to open serial port: {err}') from err

    def disconnect(self) -> bool:
        '''
            Terminates active port connection.

            :return: True if disconnected successfully, False otherwise.
            :exceptions: None.
        '''
        self._driver.close_port()
        return True

    def is_connected(self) -> bool:
        '''
            Checks if communication port is open.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._driver.is_open()

    def get_version(self) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__

    def __str__(self) -> str:
        '''
            Returns string representation of SerialPort adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
