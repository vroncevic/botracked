# -*- coding: UTF-8 -*-

'''
Module
    services_test.py
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
    Unit tests for BotServicesBundle container class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.bundle.services import BotServicesBundle
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.motion.iservice import IBotMotionService
from botracked.core.service.telemetry.iservice import IBotTelemetryService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotServicesBundleTest(TestCase):
    '''
        Defines test cases for BotServicesBundle container and methods.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''
            Verifies bundle creation and attribute preservation.

            :exceptions: None.
        '''
        conn = MagicMock(spec=IBotConnectionService)
        motion = MagicMock(spec=IBotMotionService)
        telem = MagicMock(spec=IBotTelemetryService)
        dsl = MagicMock(spec=ITbotDslService)

        bundle = BotServicesBundle(
            connection=conn,
            motion=motion,
            telemetry=telem,
            dsl=dsl,
        )

        self.assertIs(bundle.connection, conn)
        self.assertIs(bundle.motion, motion)
        self.assertIs(bundle.telemetry, telem)
        self.assertIs(bundle.dsl, dsl)
        self.assertTrue(bundle.is_initialized())

    def test_to_dict(self) -> None:
        '''
            Verifies to_dict returns dictionary containing bundle services.

            :exceptions: None.
        '''
        bundle = BotServicesBundle(
            connection=MagicMock(spec=IBotConnectionService),
            motion=MagicMock(spec=IBotMotionService),
            telemetry=MagicMock(spec=IBotTelemetryService),
            dsl=MagicMock(spec=ITbotDslService),
        )
        data = bundle.to_dict()
        self.assertIn('connection', data)
        self.assertIn('motion', data)
        self.assertIn('telemetry', data)
        self.assertIn('dsl', data)


if __name__ == '__main__':
    main()
