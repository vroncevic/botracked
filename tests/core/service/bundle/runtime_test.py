# -*- coding: UTF-8 -*-

'''
Module
    runtime_test.py
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
    Unit tests for BotRuntimeBundle composite container class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.core.service.bundle.services import BotServicesBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotRuntimeBundleTest(TestCase):
    '''
        Defines test cases for BotRuntimeBundle container and methods.
    '''

    def test_bundle_creation_and_initialization(self) -> None:
        '''
            Verifies composite bundle creation and initialization delegation.

            :exceptions: None.
        '''
        services = MagicMock(spec=BotServicesBundle)
        services.is_initialized.return_value = True
        runners = MagicMock(spec=BotRunnersBundle)
        runners.is_initialized.return_value = True

        runtime = BotRuntimeBundle(services=services, runners=runners)

        self.assertIs(runtime.services, services)
        self.assertIs(runtime.runners, runners)
        self.assertTrue(runtime.is_initialized())

        runners.is_initialized.return_value = False
        self.assertFalse(runtime.is_initialized())

    def test_to_dict(self) -> None:
        '''
            Verifies to_dict returns dictionary containing services and runners.

            :exceptions: None.
        '''
        runtime = BotRuntimeBundle(
            services=MagicMock(spec=BotServicesBundle),
            runners=MagicMock(spec=BotRunnersBundle),
        )
        data = runtime.to_dict()
        self.assertIn('services', data)
        self.assertIn('runners', data)


if __name__ == '__main__':
    main()
