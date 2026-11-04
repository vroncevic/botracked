# -*- coding: UTF-8 -*-

'''
Module
    loop.py
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
    Defines TelemetryLoop executing periodic telemetry status queries.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.protocol_opcode import ProtocolOpcode
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryLoop:
    '''
        Defines class TelemetryLoop implementing ITelemetryLoop structurally.
        Executes periodic status query loop at scheduled intervals.

        It defines:

            :attributes:
                | STATUS_FRAME_NAME - Trace label emitted for status request frames.
                | _dispatcher - Shared outbound protocol frame dispatcher port.
                | _stop_flag - Signal flag notifying loop termination.
                | _interval_sec - Poll wait interval in seconds.
            :methods:
                | __init__ - Initializes telemetry loop with injected ports.
                | run - Executes periodic status query loop until stopped.
                | is_stopped - Checks if loop stop signal is active.
    '''

    STATUS_FRAME_NAME: ClassVar[str] = 'CMD_GET_STATUS'

    _dispatcher: IFrameDispatcher
    _stop_flag: ISignalFlag
    _interval_sec: float

    def __init__(
        self,
        *,
        dispatcher: IFrameDispatcher,
        stop_flag: ISignalFlag,
        interval_sec: float,
    ) -> None:
        '''
            Initializes telemetry loop with injected collaborator ports.

            :param dispatcher: Shared outbound protocol frame dispatcher port.
            :param stop_flag: Signal flag notifying loop termination.
            :param interval_sec: Poll wait interval in seconds.
            :exceptions: None.
        '''
        self._dispatcher = dispatcher
        self._stop_flag = stop_flag
        self._interval_sec = interval_sec

    def run(self) -> None:
        '''
            Executes periodic status query loop until stopped.

            :exceptions: None.
        '''
        while not self._stop_flag.is_set():
            if self._dispatcher.can_dispatch():
                self._dispatcher.dispatch_frame(
                    ProtocolOpcode.CMD_GET_STATUS, b'', self.STATUS_FRAME_NAME
                )

            self._stop_flag.wait(self._interval_sec)

    def is_stopped(self) -> bool:
        '''
            Checks if loop stop signal is active.

            :return: True if stop flag is set, False otherwise.
            :exceptions: None.
        '''
        return self._stop_flag.is_set()
