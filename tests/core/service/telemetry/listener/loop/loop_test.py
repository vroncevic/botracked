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
    Unit tests for TelemetryListenerLoop buffered RX chunk consumption.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.queue_empty_error import QueueEmptyError
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.listener.decoder.idecoder import ITelemetryDecoder
from botracked.core.service.telemetry.listener.loop.loop import TelemetryListenerLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListenerLoopTest(TestCase):
    '''
        Verifies TelemetryListenerLoop reads from IByteReceiver and decodes chunks.
    '''

    def test_consumes_non_empty_chunks_until_stopped(self) -> None:
        '''
            Verifies non-empty chunks reach decoder while queue empty is handled.

            :exceptions: None.
        '''
        rx_port = Mock(spec=IByteReceiver)
        rx_port.read_bytes.side_effect = [b'\xaa\x05', QueueEmptyError('empty')]
        frame_decoder = Mock(spec=ITelemetryDecoder)
        rx_stop = Mock(spec=ISignalFlag)
        rx_stop.is_set.side_effect = [False, False, True, True]

        rx_loop = TelemetryListenerLoop(
            receiver=rx_port,
            decoder=frame_decoder,
            stop_flag=rx_stop,
            timeout_sec=0.05,
        )
        rx_loop.run()

        self.assertEqual(rx_port.read_bytes.call_count, 2)
        rx_port.read_bytes.assert_called_with(0.05)
        frame_decoder.decode_chunk.assert_called_once_with(b'\xaa\x05')
        self.assertTrue(rx_loop.is_stopped())


if __name__ == '__main__':
    main()
