# -*- coding: UTF-8 -*-

'''
Module
    connection_panel_config.py
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
    Provides ConnectionPanelConfig dataclass encapsulating connection panel UI literals.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class ConnectionPanelConfig:
    '''
        Defines class ConnectionPanelConfig with attribute(s) and method(s).
        Immutable UI parameters and string tokens for ConnectionPanel.

        It defines:

            :attributes:
                | default_port - Default serial port device string.
                | default_baud - Default communication baud rate string.
                | baud_rates - Tuple of selectable baud rate options.
                | padding_main - Frame padding in pixels.
                | label_port - Label text for port dropdown.
                | label_baud - Label text for baud dropdown.
                | btn_refresh - Text for port refresh button.
                | btn_connect - Text for connect button.
                | btn_disconnect - Text for disconnect button.
                | status_connected - Connected status indicator text.
                | status_disconnected - Disconnected status indicator text.
                | fallback_ports - Tuple of fallback port paths.
                | device_alias - Preferred symbolic link port path.
            :methods: None.
    '''

    default_port: str = '/dev/ttyUSB0'
    default_baud: str = '9600'
    baud_rates: tuple[str, ...] = ('115200', '57600', '9600')
    padding_main: int = 6
    label_port: str = 'Port:'
    label_baud: str = 'Baud:'
    btn_refresh: str = '↻'
    btn_connect: str = 'Connect'
    btn_disconnect: str = 'Disconnect'
    status_connected: str = 'CONNECTED'
    status_disconnected: str = 'DISCONNECTED'
    fallback_ports: tuple[str, ...] = ('/dev/ttyUSB0', '/dev/ttyACM0')
    device_alias: str = '/dev/tracked_bot'
