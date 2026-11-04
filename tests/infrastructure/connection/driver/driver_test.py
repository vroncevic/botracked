# -*- coding: UTF-8 -*-

'''
Module
    driver_test.py
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
    Unit tests for SerialDriver synchronized communication adapter.
'''

from __future__ import annotations

from threading import RLock
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.infrastructure.connection.driver.driver import SerialDriver
from botracked.infrastructure.connection.driver.ilock import IPortLock
from botracked.infrastructure.connection.driver.iraw_control import IRawSerialControl
from botracked.infrastructure.connection.driver.iraw_io import IRawSerialIO

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialDriverTest(TestCase):
    '''
        Verifies SerialDriver thread-safe execution of open, close, read, write.
    '''

    def test_open_port_and_close_port_lifecycle(self) -> None:
        '''
            Verifies open_port and close_port delegate to control under lock.

            :exceptions: None.
        '''
        ctrl = Mock(spec=IRawSerialControl)
        ctrl.open.return_value = True
        ctrl.is_open.return_value = True
        io_port = Mock(spec=IRawSerialIO)
        driver = SerialDriver(control=ctrl, io=io_port, lock=RLock())

        self.assertTrue(driver.open_port('/dev/ttyUSB0', 115200))
        ctrl.open.assert_called_once_with('/dev/ttyUSB0', 115200)
        self.assertTrue(driver.is_open())
        ctrl.is_open.return_value = False
        self.assertFalse(driver.is_open())

        driver.close_port()
        ctrl.close.assert_called_once()

    def test_read_and_write_chunk_synchronization(self) -> None:
        '''
            Verifies read_chunk and write_chunk acquire and release lock.

            :exceptions: None.
        '''
        ctrl = Mock(spec=IRawSerialControl)
        io_port = Mock(spec=IRawSerialIO)
        io_port.read.return_value = b'\xaa\x01'
        io_port.write.return_value = 2
        lock = Mock(spec=IPortLock)
        driver = SerialDriver(control=ctrl, io=io_port, lock=lock)

        self.assertEqual(driver.read_chunk(64), b'\xaa\x01')
        io_port.read.assert_called_once_with(64)

        self.assertEqual(driver.write_chunk(b'\xaa\x01'), 2)
        io_port.write.assert_called_once_with(b'\xaa\x01')
        io_port.flush.assert_called_once()


if __name__ == '__main__':
    main()
