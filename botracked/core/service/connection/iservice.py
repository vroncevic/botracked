# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines IBotConnectionService driving port for robot communication lifecycle.
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
class IBotConnectionService(Protocol):
    '''
        Defines protocol IBotConnectionService with method(s).
        Driving port orchestrating physical port and background stream workers.

        It defines:

            :methods:
                | connect - Connects communication port and starts workers.
                | disconnect - Stops workers and disconnects active port.
                | is_connected - Checks if communication port is open.
    '''

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Connects communication port and starts workers.

            :param params: Connection configuration parameters.
            :return: True if successfully connected, False otherwise.
        '''

    def disconnect(self) -> None:
        '''
            Stops workers and disconnects active port.
        '''

    def is_connected(self) -> bool:
        '''
            Checks if communication port is open.

            :return: True if active port is open, False otherwise.
        '''
