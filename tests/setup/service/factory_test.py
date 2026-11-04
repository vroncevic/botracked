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
    Unit tests for BotServiceFactory application runtime assembler.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.core.service.bundle.services import BotServicesBundle
from botracked.setup.service.factory import BotServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotServiceFactoryTestCase(TestCase):
    '''
        Tests BotServiceFactory creation and version verification.

        It defines:

            :methods:
                | test_create_service - Verifies factory creates BotRuntimeBundle.
                | test_get_version - Verifies factory returns module version string.
    '''

    def test_create_service(self) -> None:
        '''
            Verifies factory creates fully configured BotRuntimeBundle instance.

            :exceptions: None.
        '''
        runtime = BotServiceFactory.create()

        self.assertIsInstance(runtime, BotRuntimeBundle)
        self.assertIsInstance(runtime.services, BotServicesBundle)
        self.assertIsInstance(runtime.runners, BotRunnersBundle)
        self.assertTrue(runtime.is_initialized())
        self.assertIsNotNone(runtime.services.motion)
        self.assertIsNotNone(runtime.services.telemetry)
        self.assertIsNotNone(runtime.services.dsl)
        self.assertIsNotNone(runtime.runners.listener)
        self.assertIsNotNone(runtime.runners.poller)
        self.assertIsNotNone(runtime.runners.mission)
        self.assertEqual(BotServiceFactory.CRC_POLYNOMIAL, 0x07)
        self.assertFalse(runtime.services.connection.is_connected())

    def test_get_version(self) -> None:
        '''
            Verifies factory returns module version string.

            :exceptions: None.
        '''
        version = BotServiceFactory.get_version()

        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.2')


if __name__ == '__main__':
    main()
