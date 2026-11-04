# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines TelemetryPollerFactory assembling telemetry poller subsystem.
'''

from __future__ import annotations

from botracked.core.service.telemetry.poller.dependencies import TelemetryPollerDependencies
from botracked.core.service.telemetry.poller.loop.loop import TelemetryLoop
from botracked.core.service.telemetry.poller.poller import TelemetryPoller
from botracked.core.service.telemetry.poller.provides import TelemetryPollerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPollerFactory:
    '''
        Defines class TelemetryPollerFactory assembling telemetry poller subsystem.

        It defines:

            :attributes: None.
            :methods:
                | create - Creates TelemetryPollerProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: TelemetryPollerDependencies
    ) -> TelemetryPollerProvides:
        '''
            Creates TelemetryPollerProvides from TelemetryPollerDependencies.

            :param dependencies: Collaborator bundle for telemetry poller.
            :return: Assembled TelemetryPollerProvides bundle.
            :exceptions: None.
        '''
        loop = TelemetryLoop(
            dispatcher=dependencies.dispatcher,
            stop_flag=dependencies.stop_flag,
            interval_sec=dependencies.interval_sec,
        )
        poller = TelemetryPoller(
            loop=loop,
            controller=dependencies.controller,
        )
        return TelemetryPollerProvides(poller=poller)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
