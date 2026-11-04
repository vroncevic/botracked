# -*- coding: UTF-8 -*-

'''
Module
    ipoller_test.py
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
    Unit tests for ITelemetryPoller structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.core.service.telemetry.poller.loop.iloop import ITelemetryLoop
from botracked.core.service.telemetry.poller.poller import TelemetryPoller

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPollerProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of ITelemetryPoller.
    '''

    def test_conformance(self) -> None:
        '''
            Verifies TelemetryPoller satisfies ITelemetryPoller structurally.

            :exceptions: None.
        '''
        poller = TelemetryPoller(
            loop=Mock(spec=ITelemetryLoop),
            controller=Mock(spec=ILoopController),
        )
        self.assertIsInstance(poller, ITelemetryPoller)
        self.assertNotIsInstance(None, ITelemetryPoller)


if __name__ == '__main__':
    main()
