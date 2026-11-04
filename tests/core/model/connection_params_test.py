# -*- coding: UTF-8 -*-

'''
Module
    connection_params_test.py
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
    Unit tests for ConnectionParams value object.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionParamsTest(TestCase):
    '''
        Tests ConnectionParams instantiation, attributes, immutability, and equality.
    '''

    def test_instantiation_and_fields(self) -> None:
        '''
            Verifies field values upon standard instantiation.

            :exceptions: None.
        '''
        params = ConnectionParams(
            serial_port='/dev/ttyUSB0',
            baud_rate=115200,
            timeout=2.0
        )
        self.assertEqual(params.serial_port, '/dev/ttyUSB0')
        self.assertEqual(params.baud_rate, 115200)
        self.assertEqual(params.timeout, 2.0)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying frozen dataclass attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        params = ConnectionParams(
            serial_port='/dev/ttyUSB0',
            baud_rate=115200,
            timeout=1.0
        )
        with self.assertRaises(FrozenInstanceError):
            params.baud_rate = 9600  # type: ignore[misc]

    def test_equality(self) -> None:
        '''
            Verifies value object equality and inequality comparison.

            :exceptions: None.
        '''
        params1 = ConnectionParams(
            serial_port='/dev/ttyUSB0',
            baud_rate=115200,
            timeout=2.0
        )
        params2 = ConnectionParams(
            serial_port='/dev/ttyUSB0',
            baud_rate=115200,
            timeout=2.0
        )
        params3 = ConnectionParams(
            serial_port='/dev/ttyUSB1',
            baud_rate=9600,
            timeout=2.0
        )
        self.assertEqual(params1, params2)
        self.assertNotEqual(params1, params3)


if __name__ == '__main__':
    main()
