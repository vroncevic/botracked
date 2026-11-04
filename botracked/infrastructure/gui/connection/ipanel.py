# -*- coding: UTF-8 -*-

'''
Module
    ipanel.py
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
    Defines IConnectionPanel protocol for connection toolbar component.
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
class IConnectionPanel(Protocol):
    '''
        Defines structural contract IConnectionPanel for serial link toolbar.

        It defines:

            :methods:
                | get_widget - Returns root container Frame widget.
                | set_connection_state - Updates badge and interactive state.
                | refresh_ports - Refreshes available serial ports combobox.
                | on_toggle_connection - Handles connect/disconnect button action.
                | on_refresh_ports - Handles manual port refresh request.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Main Frame widget.
        '''

    def set_connection_state(self, is_connected: bool, message: str) -> None:
        '''
            Updates connection state badge and serial input controls.

            :param is_connected: True if link is active, False otherwise.
            :param message: Status badge text.
        '''

    def refresh_ports(self) -> None:
        '''
            Scans available serial ports and updates combobox list.
        '''

    def on_toggle_connection(self) -> None:
        '''
            Handles connect or disconnect button click.
        '''

    def on_refresh_ports(self) -> None:
        '''
            Handles request to refresh available serial ports.
        '''
