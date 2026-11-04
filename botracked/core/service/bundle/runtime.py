# -*- coding: UTF-8 -*-

'''
Module
    runtime.py
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
    Defines BotRuntimeBundle composing domain services and background runners.
'''

from __future__ import annotations

from dataclasses import dataclass, fields

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.bundle.services import BotServicesBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class BotRuntimeBundle:
    '''
        Defines class BotRuntimeBundle with attribute(s) and method(s).
        Composite runtime bundle holding domain services and background runners.

        It defines:

            :attributes:
                | services - Core domain application services bundle.
                | runners - Background lifecycle execution controllers bundle.
            :methods:
                | is_initialized - Checks if both sub-bundles are initialized.
                | to_dict - Converts the bundle to a dictionary.
    '''

    services: BotServicesBundle
    runners: BotRunnersBundle

    def is_initialized(self) -> bool:
        '''
            Checks if both domain services and background runners are initialized.

            :return: True if services and runners are initialized, False otherwise.
            :exceptions: None.
        '''
        return (
            self.services is not None
            and self.runners is not None
            and self.services.is_initialized()
            and self.runners.is_initialized()
        )

    def to_dict(self) -> dict[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of bundle.
            :exceptions: None.
        '''
        return {field.name: getattr(self, field.name) for field in fields(self)}
