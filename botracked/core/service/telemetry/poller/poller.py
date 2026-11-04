# -*- coding: UTF-8 -*-

'''
Module
    poller.py
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
    Defines TelemetryPoller managing background telemetry polling via ILoopController.
'''

from __future__ import annotations

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.telemetry.poller.loop.iloop import ITelemetryLoop

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPoller:
    '''
        Defines class TelemetryPoller implementing ITelemetryPoller structurally.
        Manages execution lifecycle of background telemetry status polling.

        It defines:

            :attributes:
                | _loop - Polling loop port executing periodic status requests.
                | _controller - Loop lifecycle controller port.
            :methods:
                | __init__ - Initializes poller with loop and loop controller.
                | start - Activates background telemetry polling cycle.
                | stop - Stops background telemetry polling cycle.
                | is_running - Checks if poller cycle is currently active.
    '''

    _loop: ITelemetryLoop
    _controller: ILoopController

    def __init__(
        self,
        *,
        loop: ITelemetryLoop,
        controller: ILoopController,
    ) -> None:
        '''
            Initializes poller with loop port and loop lifecycle controller.

            :param loop: Polling loop port instance.
            :param controller: Loop lifecycle controller port.
            :exceptions: None.
        '''
        self._loop = loop
        self._controller = controller

    def start(self) -> None:
        '''
            Activates background telemetry polling cycle.

            :exceptions: None.
        '''
        self._controller.start(self._loop)

    def stop(self) -> None:
        '''
            Stops background telemetry polling cycle.

            :exceptions: None.
        '''
        self._controller.stop()

    def is_running(self) -> bool:
        '''
            Checks if poller cycle is currently active.

            :return: True if controller cycle is active, False otherwise.
            :exceptions: None.
        '''
        return self._controller.is_running()
