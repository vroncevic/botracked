# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for Crc8Calculator lookup-table checksum computation.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.infrastructure.codec.crc.calculator import Crc8Calculator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Crc8CalculatorTest(TestCase):
    '''
        Verifies CRC-8 ATM checksum computation and validation.
    '''

    def test_calculate_and_version(self) -> None:
        '''
            Verifies deterministic checksum calculation and version string.

            :exceptions: None.
        '''
        calc = Crc8Calculator(polynomial=0x07)
        self.assertEqual(calc.calculate(b''), 0x00)
        crc = calc.calculate(b'\x01\x02')
        self.assertEqual(crc, calc.calculate(b'\x01\x02'))
        self.assertNotEqual(crc, calc.calculate(b'\x01\x03'))
        self.assertIsInstance(calc.get_version(), str)
        self.assertTrue(len(calc.get_version()) > 0)


if __name__ == '__main__':
    main()
