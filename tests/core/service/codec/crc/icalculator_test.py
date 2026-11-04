# -*- coding: UTF-8 -*-

'''
Module
    icalculator_test.py
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
    Unit tests for ICrc8Calculator structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.codec.crc.icalculator import ICrc8Calculator
from botracked.infrastructure.codec.crc.calculator import Crc8Calculator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Crc8CalculatorProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of ICrc8Calculator protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies Crc8Calculator satisfies ICrc8Calculator and object does not.

            :exceptions: None.
        '''
        calc = Crc8Calculator(polynomial=0x07)
        self.assertIsInstance(calc, ICrc8Calculator)
        self.assertNotIsInstance(object(), ICrc8Calculator)

    def test_mock_spec_conformance(self) -> None:
        '''
            Verifies Mock with ICrc8Calculator spec satisfies runtime check.

            :exceptions: None.
        '''
        mock_calc = Mock(spec=ICrc8Calculator)
        self.assertIsInstance(mock_calc, ICrc8Calculator)


if __name__ == '__main__':
    main()
