# -*- coding: UTF-8 -*-

'''
Module
    idecoder.py
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
    Defines structural contract ITelemetryDecoder for inbound wire decoding.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITelemetryDecoder(Protocol):
    '''
        Defines structural contract ITelemetryDecoder for inbound RX decoding.

        It defines:

            :methods:
                | reset_session - Resets framing buffer and restarts session clock.
                | decode_chunk - Decodes raw byte chunk and publishes events.
                | process_frame - Processes single decoded frame opcode/payload.
    '''

    def reset_session(self) -> None:
        '''
            Resets binary framing buffer and restarts session uptime baseline.
        '''

    def decode_chunk(self, data: bytes) -> None:
        '''
            Decodes raw byte chunk into protocol frames and publishes telemetry.

            :param data: Inbound raw byte chunk.
        '''

    def process_frame(self, opcode: int, payload: bytes) -> None:
        '''
            Processes a single decoded wire frame and notifies telemetry sink.

            :param opcode: Decoded wire frame opcode integer.
            :param payload: Decoded wire frame payload bytes.
        '''
