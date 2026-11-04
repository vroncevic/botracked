# -*- coding: UTF-8 -*-

'''
Module
    icalculator.py
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
    Defines ICrc8Calculator structural interface for cyclic redundancy checksumming.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICrc8Calculator(Protocol):
    '''
        Defines protocol ICrc8Calculator with method(s).
        Structural protocol for CRC-8 checksum calculation.

        It defines:

            :methods:
                | calculate - Calculates 8-bit CRC value for byte sequence.
                | get_version - Returns component semantic version string.
    '''

    def calculate(self, data: bytes) -> int:
        '''
            Calculates 8-bit CRC value for given byte sequence.

            :param data: Byte sequence to checksum.
            :return: Computed CRC-8 integer in range 0 to 255.
        '''

    def get_version(self) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
        '''
