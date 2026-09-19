# -*- coding: UTF-8 -*-

'''
Module
    ibot_telemetry_service.py
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
    Defines IBotTelemetryService interface for telemetry observers and state queries.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.communication.itelemetry_observer import (
    ITelemetryObserver,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBotTelemetryService(Protocol):
    '''
        Defines protocol IBotTelemetryService with method(s).
        Provides an interface for observing robot telemetry and packet activity.

        It defines:

            :methods:
                | add_observer - Registers an observer for telemetry events.
                | remove_observer - Unregisters a telemetry observer.
                | request_status - Queries telemetry status frame from robot.
                | get_telemetry - Returns most recent telemetry snapshot.
    '''

    def add_observer(self, observer: ITelemetryObserver) -> None:
        '''
            Registers an observer for telemetry and packet events.

            :param observer: Subscriber instance.
        '''

    def remove_observer(self, observer: ITelemetryObserver) -> None:
        '''
            Unregisters an observer.

            :param observer: Subscriber instance.
        '''

    def request_status(self) -> bool:
        '''
            Queries telemetry status frame from robot.

            :return: True if request sent, False otherwise.
        '''

    def get_telemetry(self) -> TelemetryData:
        '''
            Returns most recent telemetry snapshot.

            :return: Current TelemetryData.
        '''
