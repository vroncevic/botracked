# -*- coding: UTF-8 -*-

'''
Module
    dispatcher.py
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
    Defines FrameDispatcher encoding and transmitting outbound protocol frames.
'''

from __future__ import annotations

from botracked.core.model.exceptions.port_disconnected_error import PortDisconnectedError
from botracked.core.model.exceptions.transmitter_error import TransmitterError
from botracked.core.model.packet_direction import PacketDirection
from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.codec.icodec import IBinaryCodec
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


class FrameDispatcher:
    '''
        Defines class FrameDispatcher implementing IFrameDispatcher structurally.
        Encapsulates binary encoding and transmission over active robot links.

        It defines:

            :attributes:
                | _codec - Binary frame encoder and decoder.
                | _transmitter - Buffered outbound byte transmitter port.
                | _status - Narrow active connection status inspection port.
                | _sink - Narrow sink distributing packet traces to observers.
            :methods:
                | __init__ - Initializes frame dispatcher with collaborators.
                | can_dispatch - Checks whether active link is ready for dispatch.
                | dispatch_frame - Encodes opcode and payload into frame and sends.
                | dispatch_raw - Transmits pre-encoded frame and notifies sink.
    '''

    _codec: IBinaryCodec
    _transmitter: IByteTransmitter
    _status: IConnectionStatus
    _sink: ITelemetrySink

    def __init__(
        self,
        *,
        codec: IBinaryCodec,
        transmitter: IByteTransmitter,
        status: IConnectionStatus,
        sink: ITelemetrySink,
    ) -> None:
        '''
            Initializes frame dispatcher with collaborators.

            :param codec: Binary frame codec.
            :param transmitter: Buffered outbound byte transmitter port.
            :param status: Narrow active connection status inspection port.
            :param sink: Narrow sink distributing packet traces to observers.
            :exceptions: None.
        '''
        self._codec = codec
        self._transmitter = transmitter
        self._status = status
        self._sink = sink

    def can_dispatch(self) -> bool:
        '''
            Checks whether active communication link is connected and ready.

            :return: True if frames can be dispatched, False otherwise.
            :exceptions: None.
        '''
        return self._status.is_connected()

    def dispatch_frame(
        self,
        opcode: ProtocolOpcode,
        payload: bytes,
        frame_name: str,
    ) -> bool:
        '''
            Encodes opcode and payload into frame and transmits.

            :param opcode: Command operation code.
            :param payload: Command data bytes.
            :param frame_name: Frame name for logging.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        if not self.can_dispatch():
            return False

        frame: bytes = self._codec.encode_frame(opcode, payload)
        return self.dispatch_raw(frame, frame_name)

    def dispatch_raw(self, frame: bytes, frame_name: str) -> bool:
        '''
            Transmits pre-encoded frame and notifies trace sink on success.

            :param frame: Wire bytes to transmit.
            :param frame_name: Frame name for logging.
            :return: True if sent, False otherwise.
            :exceptions: None.
        '''
        if not self.can_dispatch():
            return False

        try:
            sent: bool = self._transmitter.write_bytes(frame)
        except (PortDisconnectedError, TransmitterError):
            return False

        if sent:
            self._sink.notify_packet(PacketDirection.TX, frame_name, frame)

        return sent
