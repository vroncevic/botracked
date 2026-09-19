# -*- coding: UTF-8 -*-

'''
Module
    binary_codec.py
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

from botracked.infrastructure.communication.crc8_calculator import (
    Crc8Calculator
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryCodec:
    '''
        Defines class BinaryCodec with attribute(s) and method(s).
        Encodes and decodes framed binary protocol packets for tracked_bot.

        It defines:

            :attributes:
                | _SYNC_BYTE - Synchronization start byte constant (0xAA).
                | _crc - CRC-8 calculator instance.
                | _rx_buffer - Rolling byte buffer for stream reassembly.
            :methods:
                | __init__ - Initializes codec with CRC calculator and buffer.
                | encode_frame - Encodes opcode and payload into a frame.
                | decode_stream - Processes incoming stream chunk and extracts frames.
                | reset - Clears internal receive buffer.
    '''

    _SYNC_BYTE: int = 0xAA
    _crc: Crc8Calculator
    _rx_buffer: bytearray

    def __init__(self, crc_calculator: Crc8Calculator | None = None) -> None:
        '''
            Initializes codec with CRC calculator and stream buffer.

            :param crc_calculator: Optional CRC-8 calculator instance.
            :exceptions: None.
        '''
        self._crc = crc_calculator if crc_calculator is not None else Crc8Calculator()
        self._rx_buffer = bytearray()

    def encode_frame(self, opcode: int, payload: bytes = b'') -> bytes:
        '''
            Encodes opcode and payload into a verified frame.

            :param opcode: Message ID / opcode integer (0..255).
            :param payload: Optional payload bytes.
            :return: Wire packet bytes.
            :exceptions: None.
        '''
        length: int = len(payload)
        header: bytes = bytes([self._SYNC_BYTE, opcode & 0xFF, length & 0xFF])
        protected_data: bytes = bytes([opcode & 0xFF, length & 0xFF]) + payload
        crc: int = self._crc.calculate(protected_data)
        return header + payload + bytes([crc])

    def decode_stream(self, chunk: bytes) -> list[tuple[int, bytes]]:
        '''
            Processes incoming stream chunk and extracts all valid frames.

            :param chunk: Incoming byte sequence from transport.
            :return: List of tuples containing (opcode, payload).
            :exceptions: None.
        '''
        self._rx_buffer.extend(chunk)
        frames: list[tuple[int, bytes]] = []

        while True:
            # Look for SYNC byte
            sync_index: int = self._rx_buffer.find(self._SYNC_BYTE)
            if sync_index < 0:
                self._rx_buffer.clear()
                break

            # Discard leading junk before SYNC
            if sync_index > 0:
                del self._rx_buffer[:sync_index]

            # Header check: need at least 3 bytes for [SYNC][OPCODE][LEN]
            if len(self._rx_buffer) < 3:
                break

            opcode: int = self._rx_buffer[1]
            length: int = self._rx_buffer[2]
            total_frame_len: int = 3 + length + 1  # header + payload + crc

            if len(self._rx_buffer) < total_frame_len:
                # Incomplete frame, await more bytes
                break

            payload: bytes = bytes(self._rx_buffer[3:3 + length])
            received_crc: int = self._rx_buffer[total_frame_len - 1]

            protected_data: bytes = bytes([opcode, length]) + payload
            expected_crc: int = self._crc.calculate(protected_data)

            if expected_crc == received_crc:
                frames.append((opcode, payload))
                del self._rx_buffer[:total_frame_len]
            else:
                # Corrupted frame: discard sync byte and continue search
                del self._rx_buffer[0]

        return frames

    def reset(self) -> None:
        '''
            Clears internal receive buffer.

            :exceptions: None.
        '''
        self._rx_buffer.clear()
