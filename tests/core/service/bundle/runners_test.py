# -*- coding: UTF-8 -*-

'''
Module
    runners_test.py
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
    Unit tests for BotRunnersBundle container class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotRunnersBundleTest(TestCase):
    '''
        Defines test cases for BotRunnersBundle container and methods.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''
            Verifies bundle creation and attribute preservation.

            :exceptions: None.
        '''
        listener = MagicMock(spec=ITelemetryListener)
        poller = MagicMock(spec=ITelemetryPoller)
        mission = MagicMock(spec=IMissionRunner)

        bundle = BotRunnersBundle(
            listener=listener,
            poller=poller,
            mission=mission,
        )

        self.assertIs(bundle.listener, listener)
        self.assertIs(bundle.poller, poller)
        self.assertIs(bundle.mission, mission)
        self.assertTrue(bundle.is_initialized())

    def test_to_dict(self) -> None:
        '''
            Verifies to_dict returns dictionary containing bundle runners.

            :exceptions: None.
        '''
        bundle = BotRunnersBundle(
            listener=MagicMock(spec=ITelemetryListener),
            poller=MagicMock(spec=ITelemetryPoller),
            mission=MagicMock(spec=IMissionRunner),
        )
        data = bundle.to_dict()
        self.assertIn('listener', data)
        self.assertIn('poller', data)
        self.assertIn('mission', data)


if __name__ == '__main__':
    main()
