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
    Unit tests for PortFactory subsystem assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.connection.port.iport import IConnectionPort
from botracked.core.service.connection.port.istatus import IConnectionStatus
from botracked.infrastructure.connection.driver.idriver import ISerialDriver
from botracked.infrastructure.connection.port.dependencies import PortDependencies
from botracked.infrastructure.connection.port.factory import PortFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PortFactoryTest(TestCase):
    '''
        Verifies PortFactory assembly and version reporting.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies PortFactory builds port and status interfaces.

            :exceptions: None.
        '''
        prov = PortFactory.create(
            PortDependencies(driver=Mock(spec=ISerialDriver))
        )
        self.assertIsInstance(prov.port, IConnectionPort)
        self.assertIsInstance(prov.status, IConnectionStatus)
        self.assertEqual(PortFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
