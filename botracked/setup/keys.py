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
    Runtime components and interface constraints for the botracked bundle.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from ats_utilities.base.setup.bundle import BaseBundle

from botracked.core.service.ibot_service import IBotService
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotrackedBundleKeys:
    '''
        Runtime components and interface constraints for the botracked bundle.

        It defines:

            :attributes:
                | DEPENDENCY_BASE - Key name for base bundle dependency.
                | DEPENDENCY_SERVICE - Key name for robot service dependency.
                | DEPENDENCY_GUI - Key name for GUI engine dependency.
                | DEPENDENCY_CLI - Key name for CLI adapter dependency.
                | OPTION_INFO_FILE - Key name for info file path option.
                | OPTION_PORT - Key name for hardware serial port option.
                | OPTION_BAUD - Key name for serial baud rate option.
                | OPTION_SCRIPT - Key name for mission script path option.
                | OPTION_VERBOSE - Key name for verbose logging flag option.
            :methods:
                | get_dependency_to_type - Returns dependencies to types mapping.
                | get_option_to_type - Returns options to types mapping.
    '''

    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_GUI: ClassVar[str] = 'gui'
    DEPENDENCY_CLI: ClassVar[str] = 'cli'

    OPTION_INFO_FILE: ClassVar[str] = 'info_file'
    OPTION_PORT: ClassVar[str] = 'port'
    OPTION_BAUD: ClassVar[str] = 'baud'
    OPTION_SCRIPT: ClassVar[str] = 'script'
    OPTION_VERBOSE: ClassVar[str] = 'verbose'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns mapping of bundle dependencies to their expected types.

            :return: MappingProxyType of dependency keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_BASE: BaseBundle,
            cls.DEPENDENCY_SERVICE: IBotService,
            cls.DEPENDENCY_GUI: IGUI,
            cls.DEPENDENCY_CLI: ICLI,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type | tuple[type, ...]]:
        '''
            Returns mapping of bundle options to their expected types.

            :return: MappingProxyType of option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
            cls.OPTION_PORT: str,
            cls.OPTION_BAUD: int,
            cls.OPTION_SCRIPT: str,
            cls.OPTION_VERBOSE: bool,
        })
