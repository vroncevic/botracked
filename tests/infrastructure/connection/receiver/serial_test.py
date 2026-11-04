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
    Unit tests for SerialReceiver adapter over ISerialDriver.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from serial import SerialException

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.receiver_error import ReceiverError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.receiver.serial import SerialReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialReceiverTest(TestCase):
    '''
        Verifies SerialReceiver read_bytes, is_open, and error translation.
    '''

    def test_read_bytes_states_and_errors(self) -> None:
        '''
            Verifies closed port error, valid chunk read, and ReceiverError.

            :exceptions: None.
        '''
        driver = Mock(spec=ISerialDriver)
        driver.is_open.return_value = False
        receiver = SerialReceiver(driver=driver)
        self.assertFalse(receiver.is_open())

        with self.assertRaises(PortDisconnectedError):
            receiver.read_bytes(64)

        driver.is_open.return_value = True
        self.assertTrue(receiver.is_open())
        driver.read_chunk.return_value = b'\xaa\x01'
        self.assertEqual(receiver.read_bytes(64), b'\xaa\x01')
        driver.read_chunk.assert_called_once_with(64)

        driver.read_chunk.side_effect = SerialException('broken pipe')
        with self.assertRaises(ReceiverError):
            receiver.read_bytes(64)
        self.assertIn('SerialReceiver', str(receiver))


if __name__ == '__main__':
    main()
