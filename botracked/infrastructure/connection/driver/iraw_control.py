# -*- coding: UTF-8 -*-

'''
Module
    iraw_control.py
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
    Defines structural protocol abstracting low-level serial device lifecycle.
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
class IRawSerialControl(Protocol):
    '''
        Defines structural protocol for raw serial device lifecycle control.

        It defines:

            :methods:
                | open - Opens and configures physical serial device handle.
                | close - Closes physical serial device handle.
                | is_open - Checks whether physical serial device is open.
    '''

    def open(self, port_name: str, baudrate: int) -> bool:
        '''
            Opens and configures physical serial device handle.

            :param port_name: System serial port identifier.
            :param baudrate: Communication speed in bauds.
            :return: True if device opened successfully, False otherwise.
        '''

    def close(self) -> None:
        '''
            Closes physical serial device handle.
        '''

    def is_open(self) -> bool:
        '''
            Checks whether physical serial device is open.

            :return: True if open, False otherwise.
        '''
