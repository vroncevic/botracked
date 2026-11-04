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
    Defines ITelemetryCardSection protocol for metric card grid section.
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
class ITelemetryCardSection(Protocol):
    '''
        Defines structural contract ITelemetryCardSection for telemetry cards.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | update_metrics - Updates card values from TelemetryData.
                | reset_metrics - Resets displayed cards to offline defaults.
                | get_mode_text - Returns current operating mode string.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def update_metrics(self, data: TelemetryData) -> None:
        '''
            Updates card display values from TelemetryData snapshot.

            :param data: TelemetryData instance.
        '''

    def reset_metrics(self) -> None:
        '''
            Resets displayed cards to offline defaults.
        '''

    def get_mode_text(self) -> str:
        '''
            Returns current operating mode string.

            :return: Current mode string.
        '''
