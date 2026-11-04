# -*- coding: UTF-8 -*-

'''
Module
    iinspector.py
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
    Defines ITelemetryInspector protocol interface for TelemetryData decoding.
'''

from __future__ import annotations

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
class ITelemetryInspector(Protocol):
    '''
        Defines protocol ITelemetryInspector with method(s).
        Structural protocol defining TelemetryData creation, decoding, and labeling.

        It defines:

            :methods:
                | create_offline - Creates default offline TelemetryData record.
                | decode_payload - Decodes binary status payload into TelemetryData.
                | motion_label - Formats motion command into friendly label.
    '''

    def create_offline(self) -> TelemetryData:
        '''
            Creates default offline TelemetryData record.

            :return: Default offline TelemetryData instance.
        '''

    def decode_payload(
        self, payload: bytes, *, is_connected: bool, uptime_ms: int
    ) -> TelemetryData:
        '''
            Decodes binary status payload into TelemetryData.

            :param payload: Raw bytes payload from status or diagnostic frame.
            :param is_connected: Connection state flag.
            :param uptime_ms: Connection elapsed time in milliseconds.
            :return: Decoded TelemetryData instance.
        '''

    def motion_label(self, telemetry: TelemetryData) -> str:
        '''
            Formats motion command into friendly label.

            :param telemetry: TelemetryData instance to format.
            :return: Friendly motion label string.
        '''
