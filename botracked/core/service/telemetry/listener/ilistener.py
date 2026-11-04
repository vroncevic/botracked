# -*- coding: UTF-8 -*-

'''
Module
    ilistener.py
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
    Defines structural contract ITelemetryListener for background RX listening.
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
class ITelemetryListener(Protocol):
    '''
        Defines structural contract ITelemetryListener for background RX listening.

        It defines:

            :methods:
                | start - Activates background telemetry reception listener cycle.
                | stop - Stops background telemetry reception listener cycle.
                | is_running - Checks if background listener cycle is active.
    '''

    def start(self) -> None:
        '''
            Activates background telemetry reception listener cycle.
        '''

    def stop(self) -> None:
        '''
            Stops background telemetry reception listener cycle.
        '''

    def is_running(self) -> bool:
        '''
            Checks if background listener cycle is active.

            :return: True if active, False otherwise.
        '''
