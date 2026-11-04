# -*- coding: UTF-8 -*-

'''
Module
    idispatcher.py
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
    Defines structural contract IFrameDispatcher for outbound frame transmission.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.protocol_opcode import ProtocolOpcode

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFrameDispatcher(Protocol):
    '''
        Defines protocol IFrameDispatcher with method(s).
        Structural interface for encoding and transmitting protocol frames.

        It defines:

            :methods:
                | can_dispatch - Checks whether active link is ready for dispatch.
                | dispatch_frame - Encodes opcode and payload into frame and sends.
                | dispatch_raw - Transmits pre-encoded raw frame over active link.
    '''

    def can_dispatch(self) -> bool:
        '''
            Checks whether active communication link is connected and ready.

            :return: True if frames can be dispatched, False otherwise.
        '''

    def dispatch_frame(
        self,
        opcode: ProtocolOpcode,
        payload: bytes,
        frame_name: str,
    ) -> bool:
        '''
            Encodes opcode and payload into frame and transmits over active link.

            :param opcode: Command operation code.
            :param payload: Command data bytes.
            :param frame_name: Human-readable frame description for trace logging.
            :return: True if frame was successfully transmitted, False otherwise.
        '''

    def dispatch_raw(self, frame: bytes, frame_name: str) -> bool:
        '''
            Transmits pre-encoded raw frame over active transmitter link.

            :param frame: Wire bytes to transmit.
            :param frame_name: Human-readable frame description for trace logging.
            :return: True if frame was successfully transmitted, False otherwise.
        '''
