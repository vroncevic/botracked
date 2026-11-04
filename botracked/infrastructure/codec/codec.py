# -*- coding: UTF-8 -*-

'''
Module
    codec.py
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
    Provides BinaryCodec for framing packets and decoding stream data.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.exceptions.codec_error import CodecError
from botracked.core.service.codec.crc.icalculator import ICrc8Calculator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryCodec:
    '''
        Defines class BinaryCodec implementing IBinaryCodec structurally.
        Encodes and decodes framed binary protocol packets for tracked_bot.

        It defines:

            :attributes:
                | SYNC_BYTE - Synchronization start byte constant (0xAA).
                | MIN_HEADER_LEN - Minimum header length in bytes (3).
                | MAX_PAYLOAD_LEN - Maximum payload length in bytes (255).
                | BYTE_MASK - Byte truncation mask (0xFF).
                | INDEX_OPCODE - Header offset for opcode identifier (1).
                | INDEX_LENGTH - Header offset for payload length (2).
                | CRC_LEN - Trailer length for CRC-8 checksum in bytes (1).
                | NOT_FOUND - Sentinel return code when sync byte is absent (-1).
                | DISCARD_BYTE - Byte index removed on frame validation failure (0).
                | _crc - CRC-8 calculator instance port.
                | _rx_buffer - Rolling byte buffer for stream reassembly.
            :methods:
                | __init__ - Initializes codec with CRC calculator and buffer.
                | encode_frame - Encodes opcode and payload into a frame.
                | decode_stream - Processes incoming stream chunk and extracts frames.
                | reset - Clears internal receive buffer.
    '''

    SYNC_BYTE: ClassVar[int] = 0xAA
    MIN_HEADER_LEN: ClassVar[int] = 3
    MAX_PAYLOAD_LEN: ClassVar[int] = 255
    BYTE_MASK: ClassVar[int] = 0xFF
    INDEX_OPCODE: ClassVar[int] = 1
    INDEX_LENGTH: ClassVar[int] = 2
    CRC_LEN: ClassVar[int] = 1
    NOT_FOUND: ClassVar[int] = -1
    DISCARD_BYTE: ClassVar[int] = 0

    _crc: ICrc8Calculator
    _rx_buffer: bytearray

    def __init__(self, crc_calculator: ICrc8Calculator) -> None:
        '''
            Initializes codec with CRC calculator and stream buffer.

            :param crc_calculator: CRC-8 calculator port instance.
            :exceptions: None.
        '''
        self._crc = crc_calculator
        self._rx_buffer = bytearray()

    def encode_frame(self, opcode: int, payload: bytes) -> bytes:
        '''
            Encodes opcode and payload into a verified wire frame.

            :param opcode: Message ID or opcode integer (0..255).
            :param payload: Raw payload byte sequence.
            :return: Complete wire packet bytes.
            :exceptions:
                | CodecError: If payload exceeds maximum frame length of 255 bytes.
        '''
        length: int = len(payload)

        if length > self.MAX_PAYLOAD_LEN:
            raise CodecError(
                f'Payload length {length} exceeds maximum {self.MAX_PAYLOAD_LEN}.'
            )

        masked_opcode: int = opcode & self.BYTE_MASK
        header: bytes = bytes([self.SYNC_BYTE, masked_opcode, length])
        protected_data: bytes = bytes([masked_opcode, length]) + payload
        crc: int = self._crc.calculate(protected_data)

        return header + payload + bytes([crc])

    def decode_stream(self, chunk: bytes) -> list[tuple[int, bytes]]:
        '''
            Processes incoming stream chunk and extracts all valid frames.

            :param chunk: Incoming byte sequence from communication stream.
            :return: List of tuples containing (opcode, payload).
            :exceptions: None.
        '''
        self._rx_buffer.extend(chunk)
        frames: list[tuple[int, bytes]] = []

        while True:
            sync_index: int = self._rx_buffer.find(self.SYNC_BYTE)

            if sync_index == self.NOT_FOUND:
                self._rx_buffer.clear()
                break

            if sync_index > 0:
                del self._rx_buffer[:sync_index]

            if len(self._rx_buffer) < self.MIN_HEADER_LEN:
                break

            opcode: int = self._rx_buffer[self.INDEX_OPCODE]
            length: int = self._rx_buffer[self.INDEX_LENGTH]
            total_frame_len: int = self.MIN_HEADER_LEN + length + self.CRC_LEN

            if len(self._rx_buffer) < total_frame_len:
                break

            payload: bytes = bytes(
                self._rx_buffer[self.MIN_HEADER_LEN:self.MIN_HEADER_LEN + length]
            )
            received_crc: int = self._rx_buffer[total_frame_len - self.CRC_LEN]

            protected_data: bytes = bytes([opcode, length]) + payload
            expected_crc: int = self._crc.calculate(protected_data)

            if expected_crc == received_crc:
                frames.append((opcode, payload))
                del self._rx_buffer[:total_frame_len]
            else:
                del self._rx_buffer[self.DISCARD_BYTE]

        return frames

    def reset(self) -> None:
        '''
            Clears internal receive buffer.

            :exceptions: None.
        '''
        self._rx_buffer.clear()
