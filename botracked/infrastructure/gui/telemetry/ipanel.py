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
    Defines ITelemetryPanel protocol for composite telemetry cockpit panel.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from typing import Protocol, runtime_checkable

from botracked.core.model.telemetry_data import TelemetryData

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class ITelemetryPanel(Protocol):
    '''
        Defines structural contract ITelemetryPanel for telemetry cockpit.

        It defines:

            :methods:
                | get_widget - Returns root container Frame widget.
                | update_telemetry - Updates metric cards with latest data.
                | update_packet_count - Updates total packet counter.
                | reset_telemetry - Resets metrics and packet counter.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Root container Frame.
        '''

    def update_telemetry(self, data: TelemetryData) -> None:
        '''
            Updates metric cards with latest telemetry data.

            :param data: Immutable TelemetryData snapshot.
        '''

    def update_packet_count(self, count: int) -> None:
        '''
            Updates total packet activity counter.

            :param count: Total packet count integer.
        '''

    def reset_telemetry(self) -> None:
        '''
            Resets metrics and packet counter to offline defaults.
        '''
