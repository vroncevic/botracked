# -*- coding: UTF-8 -*-

'''
Module
    studio_command_executor.py
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
    Defines StudioCommandExecutor strategy launching cockpit GUI.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists

from ats_utilities.utils.reflection import to_str

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.command.studio_command_definition import (
    StudioCommandDefinition,
)
from botracked.infrastructure.gui.engine import BotrackedGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandExecutor:
    '''
        Command strategy executing the botracked graphical cockpit interface.

        It defines:

            :attributes:
                | definition - Command definition metadata instance.
                | gui - GUI presentation engine instance.
            :methods:
                | __init__ - Initializes executor with definition and GUI engine.
                | execute - Launches GUI window.
                | get_definition - Returns definition metadata.
                | __str__ - Returns string representation of executor.
    '''

    definition: StudioCommandDefinition
    gui: BotrackedGUI

    def __init__(
        self, definition: StudioCommandDefinition, gui: BotrackedGUI
    ) -> None:
        '''
            Initializes executor with CLI definition and GUI engine.

            :param definition: Metadata definition.
            :type definition: StudioCommandDefinition

            :param gui: GUI presentation engine.
            :type gui: BotrackedGUI

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        self.definition = definition
        self.gui = gui

    def _preload_script(self, params: Mapping[str, object]) -> None:
        '''
            Preloads script file into GUI editor if specified in parameters.

            :param params: Subcommand parameters from CLI parser.
            :exceptions: None.
        '''
        script_path: object = params.get('script') or params.get('file')
        if script_path and isinstance(script_path, str) and exists(script_path):
            try:
                with open(script_path, 'r', encoding='utf-8') as script_file:
                    self.gui.load_script(script_file.read())
            except OSError:
                pass

    def execute(
        self, *, params: Mapping[str, object], service: BotService
    ) -> Mapping[str, object]:
        '''
            Launches GUI window.

            :param params: Subcommand parameters from CLI parser.
            :type params: Mapping[str, object]

            :param service: BotService core logic instance.
            :type service: BotService

            :return: Execution dictionary with returncode, stdout, stderr.
            :rtype: Mapping[str, object]

            :exceptions: None.
        '''
        if not self.gui.is_initialized() or not service.is_initialized():
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': (
                    'studio_command_executor::execute - '
                    'gui or service not initialized'
                ),
            }

        self._preload_script(params)

        try:
            self.gui.start()
            return {
                'returncode': 0,
                'stdout': 'botracked: studio session completed',
                'stderr': '',
            }
        except Exception as exc:
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': f'studio_command_executor::execute - {exc}',
            }

    def get_definition(self) -> StudioCommandDefinition:
        '''
            Returns definition metadata.

            :return: Definition instance.
            :rtype: StudioCommandDefinition

            :exceptions: None.
        '''
        return self.definition

    def __str__(self) -> str:
        '''
            Returns string representation of executor.

            :return: String.
            :rtype: str

            :exceptions: None.
        '''
        return to_str(self)
