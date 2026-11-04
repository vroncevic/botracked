# -*- coding: UTF-8 -*-

'''
Module
    iscanner.py
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
    Defines IPortScanner structural protocol for serial port discovery.
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
class IPortScanner(Protocol):
    '''
        Defines protocol IPortScanner with method(s).
        Structural port interface for discovering hardware serial ports.

        It defines:

            :methods:
                | scan_ports - Scans system for available serial ports.
                | get_version - Returns component semantic version string.
    '''

    def scan_ports(self) -> list[str]:
        '''
            Scans system for available serial communication ports.

            :return: List of device port paths (e.g. ['/dev/ttyUSB0']).
        '''

    def get_version(self) -> str:
        '''
            Returns component semantic version string.

            :return: Semantic version string.
        '''
