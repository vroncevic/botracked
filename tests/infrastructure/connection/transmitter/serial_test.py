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
    Unit tests for SerialTransmitter adapter over ISerialDriver.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.transmitter_error import TransmitterError
from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.transmitter.serial import SerialTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialTransmitterTest(TestCase):
    '''
        Verifies SerialTransmitter write_bytes completeness and error handling.
    '''

    def test_write_bytes_states_and_errors(self) -> None:
        '''
            Verifies closed port error, full/partial writes, and TransmitterError.

            :exceptions: None.
        '''
        driver = Mock(spec=ISerialDriver)
        driver.is_open.return_value = False
        tx = SerialTransmitter(driver=driver)
        self.assertFalse(tx.is_open())

        with self.assertRaises(PortDisconnectedError):
            tx.write_bytes(b'\xaa')

        driver.is_open.return_value = True
        self.assertTrue(tx.is_open())
        driver.write_chunk.side_effect = [3, 1, OSError('write failed')]

        self.assertTrue(tx.write_bytes(b'\xaa\x01\x02'))
        self.assertFalse(tx.write_bytes(b'\xaa\x01\x02'))
        with self.assertRaises(TransmitterError):
            tx.write_bytes(b'\xaa')
        self.assertIn('SerialTransmitter', str(tx))


if __name__ == '__main__':
    main()
