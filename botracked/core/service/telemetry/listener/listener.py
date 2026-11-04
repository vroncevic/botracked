# -*- coding: UTF-8 -*-

'''
Module
    listener.py
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
    Defines TelemetryListener managing background telemetry stream reception.
'''

from __future__ import annotations

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.telemetry.listener.decoder.idecoder import ITelemetryDecoder
from botracked.core.service.telemetry.listener.loop.iloop import ITelemetryListenerLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListener:
    '''
        Defines class TelemetryListener implementing ITelemetryListener structurally.
        Manages session reset and lifecycle of background inbound telemetry listening.

        It defines:

            :attributes:
                | _rx_loop - Listener loop port consuming buffered RX byte chunks.
                | _decoder - Telemetry frame stream decoder reset on session start.
                | _controller - Concurrency loop controller driving execution cycle.
            :methods:
                | __init__ - Initializes listener with loop, decoder, and controller.
                | start - Resets decoder session and activates reception cycle.
                | stop - Stops background telemetry reception cycle.
                | is_running - Checks if listener cycle is currently active.
    '''

    _rx_loop: ITelemetryListenerLoop
    _decoder: ITelemetryDecoder
    _controller: ILoopController

    def __init__(
        self,
        *,
        loop: ITelemetryListenerLoop,
        decoder: ITelemetryDecoder,
        controller: ILoopController,
    ) -> None:
        '''
            Initializes listener with loop port, decoder, and loop controller.

            :param loop: Listener loop port instance.
            :param decoder: Telemetry wire frame stream decoder port.
            :param controller: Concurrency loop controller port.
            :exceptions: None.
        '''
        self._rx_loop = loop
        self._decoder = decoder
        self._controller = controller

    def start(self) -> None:
        '''
            Stops active cycle, resets decoder session, and activates listener.

            :exceptions: None.
        '''
        self._controller.stop()
        self._decoder.reset_session()
        self._controller.start(self._rx_loop)

    def stop(self) -> None:
        '''
            Stops background telemetry reception cycle.

            :exceptions: None.
        '''
        self._controller.stop()

    def is_running(self) -> bool:
        '''
            Checks if listener cycle is currently active.

            :return: True if runner cycle is active, False otherwise.
            :exceptions: None.
        '''
        return self._controller.is_running()
