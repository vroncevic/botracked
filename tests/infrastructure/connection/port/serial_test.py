# -*- coding: UTF-8 -*-

'''
Module
    serial_test.py
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
    Unit tests for SerialPort connection lifecycle adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.port.serial import SerialPort

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortTest(TestCase):
    '''
        Verifies SerialPort connect, disconnect, and status delegation.
    '''

    def test_connect_disconnect_and_status(self) -> None:
        '''
            Verifies SerialPort delegates lifecycle operations to ISerialDriver.

            :exceptions: None.
        '''
        driver = Mock(spec=ISerialDriver)
        driver.open_port.return_value = True
        driver.is_open.return_value = True
        port = SerialPort(driver=driver)

        self.assertTrue(port.connect('/dev/ttyUSB0', 115200))
        driver.open_port.assert_called_once_with('/dev/ttyUSB0', 115200)
        self.assertTrue(port.is_connected())

        port.disconnect()
        driver.close_port.assert_called_once()
        self.assertIn('SerialPort', str(port))
        self.assertIsInstance(port.get_version(), str)
        self.assertTrue(len(port.get_version()) > 0)

        driver.open_port.side_effect = OSError('permission denied')
        with self.assertRaises(BotConnectionError):
            port.connect('/dev/ttyUSB0', 115200)


if __name__ == '__main__':
    main()
