# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines BotrackedBundle container holding primary application components.
'''

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.utils.reflection import instance_to_dict

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(slots=True, frozen=True, kw_only=True)
class BotrackedBundle:
    '''
        Container holding all primary application components for botracked.

        It defines:

            :attributes:
                | base - Base ATS bundle instance.
                | service - Core robot application services bundle.
                | gui - GUI presentation adapter contract.
                | cli - Command-line interface adapter contract.
            :methods:
                | to_dict - Converts the bundle to a dictionary.
    '''

    base: BaseBundle
    service: BotRuntimeBundle
    gui: IGUI
    cli: ICLI

    def to_dict(self) -> Mapping[str, object]:
        '''
            Converts the bundle to a dictionary representation.

            :return: Dictionary representation of bundle.
            :exceptions: None.
        '''
        return instance_to_dict(self)
