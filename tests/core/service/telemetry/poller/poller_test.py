# -*- coding: UTF-8 -*-

'''
Module
    poller_test.py
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
    Unit tests for TelemetryPoller.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.icontroller import ILoopController
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


class TelemetryPollerTestCase(TestCase):
    '''
        Verifies TelemetryPoller start, stop, and active state delegation.
    '''

    def test_start_and_stop(self) -> None:
        '''
            Verifies TelemetryPoller coordinates loop and controller cleanly.

            :exceptions: None.
        '''
        loop = Mock(spec=ITelemetryLoop)
        controller = Mock(spec=ILoopController)
        controller.is_running.side_effect = [False, True]
        poller = TelemetryPoller(loop=loop, controller=controller)

        self.assertFalse(poller.is_running())
        poller.start()
        controller.start.assert_called_once_with(loop)
        self.assertTrue(poller.is_running())

        poller.stop()
        controller.stop.assert_called_once()


if __name__ == '__main__':
    main()
