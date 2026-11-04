# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for DriverProvides provision bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.driver.provides import DriverProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DriverProvidesTest(TestCase):
    '''
        Verifies DriverProvides field storage and immutability.
    '''

    def test_fields_and_immutability(self) -> None:
        '''
            Verifies driver field retention and frozen immutability.

            :exceptions: None.
        '''
        mock_driver = Mock(spec=ISerialDriver)
        prov = DriverProvides(driver=mock_driver)
        self.assertIs(prov.driver, mock_driver)
        with self.assertRaises(FrozenInstanceError):
            prov.driver = Mock(spec=ISerialDriver)  # type: ignore[misc]


if __name__ == '__main__':
    main()
