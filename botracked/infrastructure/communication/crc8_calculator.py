# -*- coding: UTF-8 -*-

'''
Module
    crc8_calculator.py
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
    Provides Crc8Calculator implementing CRC-8 ATM polynomial (0x07).
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Crc8Calculator:
    '''
        Defines class Crc8Calculator with attribute(s) and method(s).
        Calculates standard CRC-8 ATM checksum using generator polynomial 0x07.

        It defines:

            :attributes:
                | _table - Precomputed 256-entry lookup table for CRC-8 calculation.
            :methods:
                | __init__ - Initializes lookup table for byte processing.
                | calculate - Calculates 8-bit CRC value for byte sequence.
                | update - Updates running 8-bit CRC with a single byte value.
    '''

    _table: tuple[int, ...]

    def __init__(self) -> None:
        '''
            Initializes lookup table for high-performance byte processing.

            :exceptions: None.
        '''
        table: list[int] = []
        for i in range(256):
            curr: int = i
            for _ in range(8):
                if curr & 0x80:
                    curr = ((curr << 1) ^ 0x07) & 0xFF
                else:
                    curr = (curr << 1) & 0xFF
            table.append(curr)
        self._table = tuple(table)

    def calculate(self, data: bytes) -> int:
        '''
            Calculates 8-bit CRC value for given byte sequence.

            :param data: Byte sequence to checksum.
            :return: Computed CRC-8 integer in range 0 to 255.
            :exceptions: None.
        '''
        crc: int = 0x00
        table: tuple[int, ...] = self._table
        for b in data:
            crc = table[crc ^ b]
        return crc

    def update(self, crc: int, byte: int) -> int:
        '''
            Updates running 8-bit CRC with a single byte value.

            :param crc: Running CRC integer accumulator.
            :param byte: Byte value integer to fold into CRC.
            :return: Updated CRC-8 integer in range 0 to 255.
            :exceptions: None.
        '''
        return self._table[(crc ^ byte) & 0xFF]
