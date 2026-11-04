# -*- coding: UTF-8 -*-

'''
Module
    isection.py
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
    Defines ISerialSection protocol for serial port and baud leaf UI.
'''

from __future__ import annotations

from tkinter.ttk import Frame
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
class ISerialSection(Protocol):
    '''
        Defines structural contract ISerialSection for serial input controls.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | get_port - Returns selected serial port string.
                | get_baud - Returns selected baud rate integer.
                | refresh_ports - Scans serial ports and refreshes combobox.
                | set_enabled - Enables or disables serial input widgets.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def get_port(self) -> str:
        '''
            Returns selected serial port string.

            :return: Serial port device path string.
        '''

    def get_baud(self) -> int:
        '''
            Returns selected baud rate integer.

            :return: Baud rate integer value.
        '''

    def refresh_ports(self) -> None:
        '''
            Scans serial ports and refreshes combobox items.
        '''

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables serial input controls.

            :param enabled: True if interactive, False otherwise.
        '''
