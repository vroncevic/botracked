# -*- coding: UTF-8 -*-

'''
Module
    iloop_test.py
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
    Unit tests for ITelemetryLoop structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.telemetry.poller.loop.iloop import ITelemetryLoop
from botracked.core.service.telemetry.poller.loop.loop import TelemetryLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryLoopProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of ITelemetryLoop.
    '''

    def test_poller_loop_conformance(self) -> None:
        '''
            Verifies TelemetryLoop satisfies ITelemetryLoop structurally.

            :exceptions: None.
        '''
        poller_loop = TelemetryLoop(
            dispatcher=Mock(spec=IFrameDispatcher),
            stop_flag=Mock(spec=ISignalFlag),
            interval_sec=0.1,
        )
        self.assertIsInstance(poller_loop, ITelemetryLoop)
        self.assertNotIsInstance(object(), ITelemetryLoop)


if __name__ == '__main__':
    main()
