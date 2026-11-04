# -*- coding: UTF-8 -*-

'''
Module
    ipoller.py
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
    Defines structural contract ITelemetryPoller for background status polling.
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
class ITelemetryPoller(Protocol):
    '''
        Defines structural contract ITelemetryPoller for background status polling.

        It defines:

            :methods:
                | start - Activates background telemetry polling cycle.
                | stop - Stops background telemetry polling cycle.
                | is_running - Checks if background poller cycle is active.
    '''

    def start(self) -> None:
        '''
            Activates background telemetry polling cycle.
        '''

    def stop(self) -> None:
        '''
            Stops background telemetry polling cycle.
        '''

    def is_running(self) -> bool:
        '''
            Checks if background poller cycle is active.

            :return: True if active, False otherwise.
        '''
