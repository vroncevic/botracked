# -*- coding: UTF-8 -*-

'''
Module
    codec_test.py
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
    Unit tests for BinaryCodec frame encoder and stream decoder.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.exceptions.codec_error import CodecError
from botracked.infrastructure.codec.codec import BinaryCodec
from botracked.infrastructure.codec.crc.calculator import Crc8Calculator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryCodecTest(TestCase):
    '''
        Verifies frame encoding, payload bounds, stream decoding, and buffer reset.
    '''

    _codec: BinaryCodec

    def setUp(self) -> None:
        '''
            Initializes BinaryCodec fixture with ATM CRC-8 calculator.

            :exceptions: None.
        '''
        self._codec = BinaryCodec(
            crc_calculator=Crc8Calculator(polynomial=0x07)
        )

    def test_encode_and_decode_roundtrip(self) -> None:
        '''
            Verifies encoded frame decodes back into original opcode and payload.

            :exceptions: None.
        '''
        frame = self._codec.encode_frame(0x10, b'\x01\xb4')
        decoded = self._codec.decode_stream(frame)
        self.assertEqual(decoded, [(0x10, b'\x01\xb4')])

    def test_encode_oversized_payload_raises_codec_error(self) -> None:
        '''
            Verifies payload exceeding 255 bytes raises CodecError.

            :exceptions: None.
        '''
        with self.assertRaises(CodecError):
            self._codec.encode_frame(0x10, bytes(256))

    def test_decode_fragmented_and_corrupted_stream(self) -> None:
        '''
            Verifies decoder handles noise, corrupted CRC resync, and split chunks.

            :exceptions: None.
        '''
        valid = self._codec.encode_frame(0x01, b'')
        corrupted = valid[:-1] + bytes([(valid[-1] ^ 0xFF)])
        stream = b'\x00\x99' + corrupted + valid[:2]
        self.assertEqual(self._codec.decode_stream(stream), [])
        self.assertEqual(self._codec.decode_stream(valid[2:]), [(0x01, b'')])

    def test_reset_and_str(self) -> None:
        '''
            Verifies reset clears partial bytes and str formats adapter name.

            :exceptions: None.
        '''
        partial = self._codec.encode_frame(0x02, b'\x05')[:3]
        self.assertEqual(self._codec.decode_stream(partial), [])
        self._codec.reset()
        full = self._codec.encode_frame(0x03, b'')
        self.assertEqual(self._codec.decode_stream(full), [(0x03, b'')])
        self.assertIn('BinaryCodec', str(self._codec))

    def test_firmware_frame_compatibility(self) -> None:
        '''
            Verifies exact wire compatibility with trackedbot AVR C firmware.

            :exceptions: None.
        '''
        self.assertEqual(self._codec.encode_frame(0x04, b''), b'\xaa\x04\x00\x54')
        self.assertEqual(self._codec.encode_frame(0x03, b''), b'\xaa\x03\x00\x3f')
        self.assertEqual(self._codec.encode_frame(0x10, b''), b'\xaa\x10\x00\x57')
        self.assertEqual(self._codec.encode_frame(0x11, b''), b'\xaa\x11\x00\x42')
        self.assertEqual(self._codec.encode_frame(0x12, b''), b'\xaa\x12\x00\x7d')
        self.assertEqual(
            self._codec.encode_frame(0x01, bytes([0x01])), b'\xaa\x01\x01\x01\x79'
        )
        self.assertEqual(
            self._codec.decode_stream(b'\xaa\x84\x00\xe2'), [(0x84, b'')]
        )
        self.assertEqual(
            self._codec.decode_stream(
                b'\xaa\x90\x07\x00\x00\x00\x00\x00\x00\xb4\xcd'
            ),
            [(0x90, b'\x00\x00\x00\x00\x00\x00\xb4')],
        )


if __name__ == '__main__':
    main()
