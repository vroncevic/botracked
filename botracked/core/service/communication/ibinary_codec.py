# -*- coding: UTF-8 -*-

'''
Module
    ibinary_codec.py
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
    Defines IBinaryCodec interface for framing, encoding, and stream decoding.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryCodec(Protocol):
    '''
        Defines protocol IBinaryCodec with method(s).
        Protocol for framing outbound packets and decoding incoming byte streams.

        It defines:

            :methods:
                | encode_frame - Encodes opcode and payload into a framed packet.
                | decode_stream - Ingests stream chunk and extracts validated frames.
    '''

    def encode_frame(self, opcode: int, payload: bytes = b'') -> bytes:
        '''
            Encodes opcode and payload into a framed packet:
            [SYNC 0xAA][OPCODE: 1B][LEN: 1B][PAYLOAD: 0..NB][CRC8: 1B]

            :param opcode: Command or response ID.
            :param payload: Optional payload bytes.
            :return: Complete wire frame bytes.
        '''

    def decode_stream(self, chunk: bytes) -> list[tuple[int, bytes]]:
        '''
            Ingests a stream chunk and extracts all valid validated frames.

            :param chunk: Raw byte sequence received from transport.
            :return: List of tuples (opcode, payload) for each verified frame.
        '''
