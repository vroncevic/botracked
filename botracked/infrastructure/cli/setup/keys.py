# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the CLI bundle.
'''

from __future__ import annotations

from collections.abc import Sequence
from types import MappingProxyType
from typing import ClassVar

from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.gui.engine import BotrackedGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleKeys:
    '''
        Runtime components and interface constraints for the CLI bundle.

        It defines:

            :attributes:
                | DEPENDENCY_SERVICE - Service key for the CLI bundle.
                | DEPENDENCY_PARSER - Parser key for the CLI bundle.
                | DEPENDENCY_COMMANDS - Commands sequence key for the CLI bundle.
                | OPTION_SERVICE - Service option key for the CLI bundle.
                | OPTION_GUI - GUI presentation option key for the CLI bundle.
                | OPTION_PARSER - Parser option key for the CLI bundle.
            :methods:
                | get_dependency_to_type - Returns mapping of CLI dependencies to types.
                | get_option_to_type - Returns mapping of CLI options to types.
    '''

    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_PARSER: ClassVar[str] = 'parser'
    DEPENDENCY_COMMANDS: ClassVar[str] = 'commands'

    OPTION_SERVICE: ClassVar[str] = 'service'
    OPTION_GUI: ClassVar[str] = 'gui'
    OPTION_PARSER: ClassVar[str] = 'parser'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns mapping of CLI bundle dependencies to their expected types.

            :return: MappingProxyType of dependency keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_SERVICE: BotService,
            cls.DEPENDENCY_PARSER: IOptionManager,
            cls.DEPENDENCY_COMMANDS: Sequence,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns mapping of CLI bundle options to their expected types.

            :return: MappingProxyType of option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_SERVICE: BotService,
            cls.OPTION_GUI: BotrackedGUI,
            cls.OPTION_PARSER: IOptionManager,
        })
