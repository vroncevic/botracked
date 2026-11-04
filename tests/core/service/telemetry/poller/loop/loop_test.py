# -*- coding: UTF-8 -*-

'''
Module
    loop_test.py
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
    Unit tests for TelemetryLoop periodic status query execution.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.telemetry.poller.loop.loop import TelemetryLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryLoopTest(TestCase):
    '''
        Verifies TelemetryLoop periodic polling when ready and disconnected.
    '''

    def test_run_polls_when_ready_and_waits(self) -> None:
        '''
            Verifies dispatch_frame runs only when can_dispatch is True.

            :exceptions: None.
        '''
        dispatcher = Mock(spec=IFrameDispatcher)
        dispatcher.can_dispatch.side_effect = [True, False]
        stop_signal = Mock(spec=ISignalFlag)
        stop_signal.is_set.side_effect = [False, False, True, True]

        poller_loop = TelemetryLoop(
            dispatcher=dispatcher,
            stop_flag=stop_signal,
            interval_sec=0.05,
        )
        poller_loop.run()

        dispatcher.dispatch_frame.assert_called_once_with(
            ProtocolOpcode.CMD_GET_STATUS, b'', 'CMD_GET_STATUS'
        )
        self.assertEqual(stop_signal.wait.call_count, 2)
        self.assertTrue(poller_loop.is_stopped())


if __name__ == '__main__':
    main()
