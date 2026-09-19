# -*- coding: UTF-8 -*-

'''
Module
    binary_codec_test.py
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
    Unit tests for binary framing, CRC-8, and packet encoding/decoding.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.infrastructure.communication.binary_codec import (
    BinaryCodec,
)
from botracked.infrastructure.communication.crc8_calculator import (
    Crc8Calculator,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryCodec(TestCase):
    '''
    Tests encoding and decoding of binary protocol frames.
    '''

    _codec: BinaryCodec

    def setUp(self) -> None:
        self._codec = BinaryCodec()

    def test_crc8_calculation(self) -> None:
        '''
        Verifies CRC-8 ATM polynomial matches specification.
        '''
        crc_calc = Crc8Calculator()
        # [MSG_ID=0x04, LEN=0x00] -> CRC=0x54
        crc = crc_calc.calculate(bytes([0x04, 0x00]))
        self.assertEqual(crc, 0x54)

    def test_encode_ping(self) -> None:
        '''
        Verifies ping frame matches 0xAA 0x04 0x00 0x54.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_PING)
        self.assertEqual(frame, bytes([0xAA, 0x04, 0x00, 0x54]))

    def test_encode_stop(self) -> None:
        '''
        Verifies stop frame format.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_STOP)
        self.assertEqual(frame[0], 0xAA)
        self.assertEqual(frame[1], ProtocolOpcode.CMD_STOP)
        self.assertEqual(frame[2], 0x00)

    def test_encode_set_speed(self) -> None:
        '''
        Verifies set speed frame with payload.
        '''
        frame = self._codec.encode_frame(ProtocolOpcode.CMD_SET_SPEED, bytes([200]))
        self.assertEqual(frame[0], 0xAA)
        self.assertEqual(frame[1], ProtocolOpcode.CMD_SET_SPEED)
        self.assertEqual(frame[2], 0x01)
        self.assertEqual(frame[3], 200)

    def test_decode_valid_frame(self) -> None:
        '''
        Verifies decoding of valid response packet.
        '''
        # ACK frame: 0xAA 0x80 0x00 CRC
        crc_calc = Crc8Calculator()
        payload_data = bytes([0x80, 0x00])
        crc = crc_calc.calculate(payload_data)
        raw = bytes([0xAA, 0x80, 0x00, crc])

        frames = self._codec.decode_stream(raw)
        self.assertEqual(len(frames), 1)
        opcode, payload = frames[0]
        self.assertEqual(opcode, ProtocolOpcode.RESP_ACK)
        self.assertEqual(payload, b'')

    def test_decode_status_frame(self) -> None:
        '''
        Verifies decoding of valid RESP_STATUS frame from robot.
        '''
        crc_calc = Crc8Calculator()
        payload = bytes([0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0xB4])
        header_payload = bytes([ProtocolOpcode.RESP_STATUS, len(payload)]) + payload
        crc = crc_calc.calculate(header_payload)
        raw = bytes([0xAA]) + header_payload + bytes([crc])

        frames = self._codec.decode_stream(raw)
        self.assertEqual(len(frames), 1)
        opcode, decoded_payload = frames[0]
        self.assertEqual(opcode, ProtocolOpcode.RESP_STATUS)
        self.assertEqual(decoded_payload, payload)


if __name__ == '__main__':
    main()
