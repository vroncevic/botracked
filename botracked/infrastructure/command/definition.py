# -*- coding: UTF-8 -*-

'''
Module
    definition.py
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
    Defines StudioCommandDefinition CLI subcommand metadata.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandDefinition:
    '''
        CLI subcommand metadata definition for botracked cockpit and mission
        studio.

        It defines:

            :attributes:
                | COMMAND_NAME - Subcommand identifier string.
                | HELP_DESCRIPTION - Subcommand help summary text.
                | DEFAULT_PORT - Default hardware serial device path.
                | DEFAULT_BAUD - Default serial baud rate string.
                | name - Command name property.
                | help_text - Command help description property.
                | options - CLI option specifications sequence property.
            :methods:
                | __str__ - Returns string representation of definition.
    '''

    COMMAND_NAME: ClassVar[str] = 'studio'
    HELP_DESCRIPTION: ClassVar[str] = (
        'Launch botracked robot cockpit and mission scripting studio'
    )
    DEFAULT_PORT: ClassVar[str] = '/dev/ttyUSB0'
    DEFAULT_BAUD: ClassVar[str] = '9600'

    @property
    def name(self) -> str:
        '''
            Returns command name.

            :return: String name.
            :exceptions: None.
        '''
        return self.COMMAND_NAME

    @property
    def help_text(self) -> str:
        '''
            Returns command help description.

            :return: Help string.
            :exceptions: None.
        '''
        return self.HELP_DESCRIPTION

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns CLI option specifications.

            :return: Sequence of OptionData instances.
            :exceptions: None.
        '''
        return (
            OptionData(
                name='--port',
                help_text='Hardware serial port device (e.g. /dev/ttyUSB0)',
                action=None,
                default=self.DEFAULT_PORT,
                required=False,
                choices=None,
                nargs=None,
            ),
            OptionData(
                name='--baud',
                help_text='Serial baud rate (e.g. 9600)',
                action=None,
                default=self.DEFAULT_BAUD,
                required=False,
                choices=None,
                nargs=None,
            ),
            OptionData(
                name='--script',
                help_text='Path to .track mission script to preload',
                action=None,
                default='',
                required=False,
                choices=None,
                nargs=None,
            ),
            OptionData(
                name='--verbose',
                help_text='Enable verbose logging',
                action='store_true',
                default=False,
                required=False,
                choices=None,
                nargs=None,
            ),
        )

    def __str__(self) -> str:
        '''
            Returns string representation of definition.

            :return: String.
            :exceptions: None.
        '''
        return to_str(self)
