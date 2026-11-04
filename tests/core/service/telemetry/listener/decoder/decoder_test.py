# -*- coding: UTF-8 -*-

'''
Module
    decoder_test.py
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
    Unit tests for TelemetryDecoder frame decoding and sink notifications.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.listener.decoder.decoder import TelemetryDecoder
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryDecoderTest(TestCase):
    '''
        Verifies TelemetryDecoder wire chunk decoding and telemetry broadcasting.
    '''

    def test_decode_chunk_status_diag_and_unknown_opcode(self) -> None:
        '''
            Verifies RESP_STATUS, RESP_DIAG, and unknown opcode frame handling.

            :exceptions: None.
        '''
        codec = Mock(spec=IBinaryCodec)
        codec.decode_stream.return_value = [
            (int(ProtocolOpcode.RESP_STATUS), b'\x01\x02'),
            (int(ProtocolOpcode.RESP_DIAG), b'\x03\x04'),
            (0xFE, b'\x99'),
        ]
        snapshot = TelemetryData(
            system_mode='NORMAL',
            motion=MotionCommand.FORWARD,
            speed_pwm=180,
            error_code=0,
            uptime_ms=50,
            left_motor_state='FWD',
            right_motor_state='FWD',
            last_updated=10.0,
            is_connected=True,
        )
        inspector = Mock(spec=ITelemetryInspector)
        inspector.decode_payload.return_value = snapshot
        sink = Mock(spec=ITelemetrySink)
        clock = Mock(spec=IClock)
        clock.monotonic.side_effect = [100.0, 100.05, 100.1, 200.0]

        decoder = TelemetryDecoder(
            codec=codec, inspector=inspector, sink=sink, clock=clock
        )
        decoder.decode_chunk(b'\xaa\xbb')
        decoder.reset_session()

        codec.reset.assert_called_once()
        codec.decode_stream.assert_called_once_with(b'\xaa\xbb')
        self.assertEqual(sink.notify_packet.call_count, 3)
        sink.notify_packet.assert_any_call(PacketDirection.RX, 'RESP_STATUS', b'\x01\x02')
        sink.notify_packet.assert_any_call(PacketDirection.RX, 'RESP_DIAG', b'\x03\x04')
        sink.notify_packet.assert_any_call(PacketDirection.RX, '0xFE', b'\x99')
        self.assertEqual(inspector.decode_payload.call_count, 2)
        self.assertEqual(sink.notify_telemetry.call_count, 2)


if __name__ == '__main__':
    main()
