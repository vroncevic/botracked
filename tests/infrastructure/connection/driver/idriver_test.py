# -*- coding: UTF-8 -*-

'''
Module
    idriver_test.py
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
    Unit tests for ISerialDriver structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.infrastructure.connection.driver.driver import SerialDriver
from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.driver.ilock import IPortLock
from botracked.infrastructure.connection.driver.iraw_control import IRawSerialControl
from botracked.infrastructure.connection.driver.iraw_io import IRawSerialIO

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialDriverProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of ISerialDriver.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies SerialDriver satisfies ISerialDriver and object does not.

            :exceptions: None.
        '''
        driver = SerialDriver(
            control=Mock(spec=IRawSerialControl),
            io=Mock(spec=IRawSerialIO),
            lock=Mock(spec=IPortLock),
        )
        self.assertIsInstance(driver, ISerialDriver)
        self.assertNotIsInstance(object(), ISerialDriver)


if __name__ == '__main__':
    main()
