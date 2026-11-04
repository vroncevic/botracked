# -*- coding: UTF-8 -*-

'''
Module
    listener_test.py
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
    Unit tests for TelemetryListener lifecycle management.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.telemetry.listener.decoder.idecoder import ITelemetryDecoder
from botracked.core.service.telemetry.listener.listener import TelemetryListener
from botracked.core.service.telemetry.listener.loop.iloop import ITelemetryListenerLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListenerTest(TestCase):
    '''
        Verifies TelemetryListener background thread activation and stopping.
    '''

    def test_listener_lifecycle_transitions(self) -> None:
        '''
            Verifies start resets decoder session and activates loop, and stop halts.

            :exceptions: None.
        '''
        rx_loop = Mock(spec=ITelemetryListenerLoop)
        rx_decoder = Mock(spec=ITelemetryDecoder)
        rx_ctrl = Mock(spec=ILoopController)
        rx_ctrl.is_running.return_value = True
        rx_listener = TelemetryListener(
            loop=rx_loop, decoder=rx_decoder, controller=rx_ctrl
        )

        rx_listener.start()
        rx_decoder.reset_session.assert_called_once()
        rx_ctrl.start.assert_called_once_with(rx_loop)
        self.assertTrue(rx_listener.is_running())

        rx_ctrl.is_running.return_value = False
        rx_listener.stop()
        self.assertFalse(rx_listener.is_running())
        self.assertEqual(rx_ctrl.stop.call_count, 2)


if __name__ == '__main__':
    main()
