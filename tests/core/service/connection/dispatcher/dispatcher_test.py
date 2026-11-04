# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit tests for FrameDispatcher.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.transmitter_error import TransmitterError
from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.connection.dispatcher.dispatcher import FrameDispatcher
from botracked.core.service.connection.port.istatus import IConnectionStatus
from botracked.core.service.connection.transmitter.protocol.itransmitter import IByteTransmitter
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDispatcherTestCase(TestCase):
    '''
        Verifies FrameDispatcher encoding, transmission, and disconnect safety.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.codec = Mock(spec=IBinaryCodec)
        self.tx = Mock(spec=IByteTransmitter)
        self.status = Mock(spec=IConnectionStatus)
        self.status.is_connected.return_value = True
        self.sink = Mock(spec=ITelemetrySink)
        self.dispatcher = FrameDispatcher(
            codec=self.codec,
            transmitter=self.tx,
            status=self.status,
            sink=self.sink,
        )

    def test_dispatch_frame_and_raw_outcomes(self) -> None:
        '''
            Verifies can_dispatch, dispatch_frame, and dispatch_raw outcomes.

            :exceptions: None.
        '''
        self.assertTrue(self.dispatcher.can_dispatch())
        self.codec.encode_frame.return_value = b'\xaa\x01\x00'
        self.tx.write_bytes.return_value = True
        self.assertTrue(
            self.dispatcher.dispatch_frame(
                ProtocolOpcode.CMD_STOP, b'', 'CMD_STOP'
            )
        )
        self.sink.notify_packet.assert_called_once_with(
            PacketDirection.TX, 'CMD_STOP', b'\xaa\x01\x00'
        )

        self.tx.write_bytes.return_value = False
        self.assertFalse(self.dispatcher.dispatch_raw(b'\xaa', 'NOT_SENT'))
        self.assertEqual(self.sink.notify_packet.call_count, 1)

        self.tx.write_bytes.side_effect = PortDisconnectedError('lost')
        self.assertFalse(self.dispatcher.dispatch_raw(b'\xaa', 'LOST'))

        self.tx.write_bytes.side_effect = TransmitterError('tx_err')
        self.assertFalse(self.dispatcher.dispatch_raw(b'\xaa', 'TX_ERR'))

        self.status.is_connected.return_value = False
        self.assertFalse(self.dispatcher.can_dispatch())
        self.assertFalse(
            self.dispatcher.dispatch_frame(
                ProtocolOpcode.CMD_STOP, b'', 'OFF_FRAME'
            )
        )
        self.assertFalse(self.dispatcher.dispatch_raw(b'\xaa', 'OFF_RAW'))


if __name__ == '__main__':
    main()
