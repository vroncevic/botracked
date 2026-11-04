# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for CrcFactory subsystem assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.service.codec.crc.icalculator import ICrc8Calculator
from botracked.infrastructure.codec.crc.dependencies import CrcDependencies
from botracked.infrastructure.codec.crc.factory import CrcFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CrcFactoryTest(TestCase):
    '''
        Verifies CrcFactory assembly and version reporting.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies CrcFactory builds ICrc8Calculator provider and returns version.

            :exceptions: None.
        '''
        prov = CrcFactory.create(CrcDependencies(polynomial=0x07))
        self.assertIsInstance(prov.calculator, ICrc8Calculator)
        self.assertEqual(CrcFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
