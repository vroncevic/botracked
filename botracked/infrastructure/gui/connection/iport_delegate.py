# -*- coding: UTF-8 -*-

'''
Module
    iport_delegate.py
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
    Defines narrow IPortRefreshDelegate protocol for serial port scanning.
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
class IPortRefreshDelegate(Protocol):
    '''
        Defines structural contract IPortRefreshDelegate for port discovery.

        It defines:

            :methods:
                | handle_refresh_ports - Scans and returns serial port paths.
                | has_available_ports - Checks whether any serial port exists.
    '''

    def handle_refresh_ports(self) -> tuple[str, ...]:
        '''
            Scans and returns detected serial port device paths.

            :return: Tuple of port device path strings.
        '''

    def has_available_ports(self) -> bool:
        '''
            Checks whether at least one serial port is currently detected.

            :return: True if one or more ports are detected, False otherwise.
        '''
