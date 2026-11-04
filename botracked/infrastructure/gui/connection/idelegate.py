# -*- coding: UTF-8 -*-

'''
Module
    idelegate.py
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
    Defines IConnectionActionDelegate protocol for link connect/disconnect.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.connection_params import ConnectionParams

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IConnectionActionDelegate(Protocol):
    '''
        Defines structural contract IConnectionActionDelegate for serial link UI.

        It defines:

            :methods:
                | handle_connect - Opens serial link and returns status tuple.
                | handle_disconnect - Closes active serial link cleanly.
                | handle_refresh_ports - Scans available hardware serial ports.
    '''

    def handle_connect(self, params: ConnectionParams) -> tuple[bool, str]:
        '''
            Initiates serial link connection and reports outcome.

            :param params: Serial connection configuration parameters.
            :return: Tuple of connection boolean state and status badge text.
        '''

    def handle_disconnect(self) -> None:
        '''
            Terminates active serial link connection and aborts missions.
        '''

    def handle_refresh_ports(self) -> tuple[str, ...]:
        '''
            Scans and retrieves available serial ports.

            :return: Tuple of detected port device path strings.
        '''
