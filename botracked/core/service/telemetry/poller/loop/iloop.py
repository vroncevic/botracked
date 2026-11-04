# -*- coding: UTF-8 -*-

'''
Module
    iloop.py
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
    Defines structural contract ITelemetryLoop for periodic status query loops.
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
class ITelemetryLoop(Protocol):
    '''
        Defines structural contract ITelemetryLoop for periodic telemetry polling.

        It defines:

            :methods:
                | run - Executes periodic status query loop until stopped.
                | is_stopped - Checks if loop stop signal flag is active.
    '''

    def run(self) -> None:
        '''
            Executes periodic status query loop until stopped.
        '''

    def is_stopped(self) -> bool:
        '''
            Checks if loop stop signal flag is active.

            :return: True if stop flag is set, False otherwise.
        '''
