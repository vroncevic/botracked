# -*- coding: UTF-8 -*-

'''
Module
    control_test.py
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
    Unit tests for RawSerialControl adapter over pyserial Serial primitive.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock
from serial import Serial

from botracked.infrastructure.connection.driver.control import RawSerialControl

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RawSerialControlTest(TestCase):
    '''
        Verifies RawSerialControl open, close, is_open, and __str__ operations.
    '''

    def test_open_close_and_is_open(self) -> None:
        '''
            Verifies open configures and opens serial port, and close terminates it.

            :exceptions: None.
        '''
        mock_serial = Mock(spec=Serial)
        mock_serial.is_open = True
        ctrl = RawSerialControl(mock_serial)

        self.assertTrue(ctrl.is_open())
        self.assertTrue(ctrl.open('/dev/ttyUSB0', 115200))
        mock_serial.close.assert_called_once()
        self.assertEqual(mock_serial.port, '/dev/ttyUSB0')
        self.assertEqual(mock_serial.baudrate, 115200)
        mock_serial.open.assert_called_once()

        ctrl.close()
        self.assertEqual(mock_serial.close.call_count, 2)
        self.assertIn('RawSerialControl', str(ctrl))

    def test_open_and_close_when_already_closed(self) -> None:
        '''
            Verifies open and close do not close when already closed.

            :exceptions: None.
        '''
        mock_serial = Mock(spec=Serial)
        mock_serial.is_open = False
        ctrl = RawSerialControl(mock_serial)

        self.assertFalse(ctrl.is_open())
        ctrl.close()
        mock_serial.close.assert_not_called()


if __name__ == '__main__':
    main()
