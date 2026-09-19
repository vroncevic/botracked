# -*- coding: UTF-8 -*-

'''
Module
    ibot_service.py
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
    Defines composite IBotService interface for core robot orchestration.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.service.ibot_connection_service import (
    IBotConnectionService,
)
from botracked.core.service.ibot_mission_service import IBotMissionService
from botracked.core.service.ibot_motion_service import IBotMotionService
from botracked.core.service.ibot_telemetry_service import IBotTelemetryService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBotService(
    IBotConnectionService,
    Protocol
):
    '''
        Defines protocol IBotService with method(s).
        Primary application service interface for controlling and monitoring tracked_bot.

        It defines:

            :methods:
                | is_initialized - Checks if service is initialized.
                | get_motion - Returns active motion and actuation service.
                | get_telemetry - Returns active telemetry and observer service.
                | get_mission_runner - Returns background mission execution worker.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if service is initialized.

            :return: True if ready, False otherwise.
        '''

    def get_motion(self) -> IBotMotionService:
        '''
            Returns active motion and actuation service.

            :return: IBotMotionService instance.
        '''

    def get_telemetry(self) -> IBotTelemetryService:
        '''
            Returns active telemetry and observer service.

            :return: IBotTelemetryService instance.
        '''

    def get_mission_runner(self) -> IBotMissionService:
        '''
            Returns background mission execution worker.

            :return: IBotMissionService instance.
        '''
