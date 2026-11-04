# -*- coding: UTF-8 -*-

'''
Module
    services.py
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
    Defines BotServicesBundle container holding core domain application services.
'''

from __future__ import annotations

from dataclasses import dataclass, fields

from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.motion.iservice import IBotMotionService
from botracked.core.service.telemetry.iservice import IBotTelemetryService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class BotServicesBundle:
    '''
        Defines class BotServicesBundle with attribute(s) and method(s).
        Container bundle holding strictly core domain application services.

        It defines:

            :attributes:
                | connection - Link connection management service.
                | motion - Kinematic actuation and motion command service.
                | telemetry - Telemetry observer dispatch and trace service.
                | dsl - Mission DSL lexing, parsing, and compilation service.
            :methods:
                | is_initialized - Checks if all bundled services are initialized.
                | to_dict - Converts the bundle to a dictionary.
    '''

    connection: IBotConnectionService
    motion: IBotMotionService
    telemetry: IBotTelemetryService
    dsl: ITbotDslService

    def is_initialized(self) -> bool:
        '''
            Checks if all bundled services are initialized.

            :return: True if all services are initialized, False otherwise.
            :exceptions: None.
        '''
        return (
            self.connection is not None
            and self.motion is not None
            and self.telemetry is not None
            and self.dsl is not None
        )

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of bundle.
            :exceptions: None.
        '''
        return {field.name: getattr(self, field.name) for field in fields(self)}
