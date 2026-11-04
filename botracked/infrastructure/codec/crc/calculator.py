# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Provides Crc8Calculator implementing configurable 8-bit CRC calculation.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Crc8Calculator:
    '''
        Defines class Crc8Calculator implementing ICrc8Calculator structurally.
        Calculates 8-bit CRC checksum using precomputed 256-entry lookup table.

        It defines:

            :attributes:
                | DEFAULT_POLYNOMIAL - Standard CRC-8 ATM generator polynomial (0x07).
                | TABLE_SIZE - Number of lookup table entries (256).
                | BITS_PER_BYTE - Number of bit shifts per byte entry (8).
                | MSB_MASK - Most significant bit mask for 8-bit integer (0x80).
                | BYTE_MASK - Byte truncation mask (0xFF).
                | INITIAL_CRC - Initial accumulator value (0x00).
                | _table - Precomputed 256-entry lookup table for CRC-8 calculation.
            :methods:
                | __init__ - Initializes lookup table for specified polynomial.
                | calculate - Calculates 8-bit CRC value for byte sequence.
                | get_version - Returns component semantic version string.
    '''

    DEFAULT_POLYNOMIAL: ClassVar[int] = 0x07
    TABLE_SIZE: ClassVar[int] = 256
    BITS_PER_BYTE: ClassVar[int] = 8
    MSB_MASK: ClassVar[int] = 0x80
    BYTE_MASK: ClassVar[int] = 0xFF
    INITIAL_CRC: ClassVar[int] = 0x00

    _table: tuple[int, ...]

    def __init__(self, *, polynomial: int) -> None:
        '''
            Initializes lookup table for high-performance byte processing.

            :param polynomial: 8-bit generator polynomial integer.
            :exceptions: None.
        '''
        table: list[int] = []

        for index in range(self.TABLE_SIZE):
            curr: int = index

            for _ in range(self.BITS_PER_BYTE):
                if curr & self.MSB_MASK:
                    curr = ((curr << 1) ^ polynomial) & self.BYTE_MASK
                else:
                    curr = (curr << 1) & self.BYTE_MASK

            table.append(curr)

        self._table = tuple(table)

    def calculate(self, data: bytes) -> int:
        '''
            Calculates 8-bit CRC value for given byte sequence.

            :param data: Byte sequence to checksum.
            :return: Computed CRC-8 integer in range 0 to 255.
            :exceptions: None.
        '''
        crc: int = self.INITIAL_CRC
        table: tuple[int, ...] = self._table

        for byte_val in data:
            crc = table[crc ^ byte_val]

        return crc

    def get_version(self) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
