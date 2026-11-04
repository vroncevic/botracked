# -*- coding: UTF-8 -*-

'''
Module
    runners.py
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
    Defines BotRunnersBundle container holding background lifecycle controllers.
'''

from __future__ import annotations

from dataclasses import dataclass, fields

from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class BotRunnersBundle:
    '''
        Defines class BotRunnersBundle with attribute(s) and method(s).
        Container bundle holding background lifecycle execution controllers.

        It defines:

            :attributes:
                | listener - Background inbound telemetry stream listener.
                | poller - Background periodic telemetry status poller.
                | mission - Asynchronous mission routine execution runner.
            :methods:
                | is_initialized - Checks if all bundled runners are initialized.
                | to_dict - Converts the bundle to a dictionary.
    '''

    listener: ITelemetryListener
    poller: ITelemetryPoller
    mission: IMissionRunner

    def is_initialized(self) -> bool:
        '''
            Checks if all bundled runners are initialized.

            :return: True if all runners are initialized, False otherwise.
            :exceptions: None.
        '''
        return (
            self.listener is not None
            and self.poller is not None
            and self.mission is not None
        )

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of bundle.
            :exceptions: None.
        '''
        return {field.name: getattr(self, field.name) for field in fields(self)}
