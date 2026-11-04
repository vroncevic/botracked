# -*- coding: UTF-8 -*-

'''
Module
    executor.py
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
from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.command.idefinition import ICommandDefinition
from botracked.infrastructure.command.ipreloader import IScriptPreloader
from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandExecutor:
    '''
        Command strategy executing the botracked graphical cockpit interface.

        It defines:

            :attributes:
                | EXIT_SUCCESS - Process success return code.
                | EXIT_FAILURE - Process failure return code.
                | _definition - Command definition metadata contract.
                | _gui - GUI presentation engine contract.
                | _preloader - Script file preloader contract.
            :methods:
                | __init__ - Initializes executor with definition, GUI, and preloader.
                | execute - Launches GUI window.
                | get_definition - Returns definition metadata.
                | __str__ - Returns string representation of executor.
    '''

    EXIT_SUCCESS: ClassVar[int] = 0
    EXIT_FAILURE: ClassVar[int] = 1

    _definition: ICommandDefinition
    _gui: IGUI
    _preloader: IScriptPreloader

    def __init__(
        self,
        definition: ICommandDefinition,
        gui: IGUI,
        preloader: IScriptPreloader,
    ) -> None:
        '''
            Initializes executor with CLI definition, GUI engine, and preloader.

            :param definition: Command metadata definition contract.
            :param gui: GUI presentation engine contract.
            :param preloader: Script preloader collaborator contract.
            :exceptions: None.
        '''
        self._definition = definition
        self._gui = gui
        self._preloader = preloader

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: BotRuntimeBundle,
    ) -> Mapping[str, object]:
        '''
            Launches GUI window.

            :param params: Subcommand parameters from CLI parser.
            :param service: Core robot application services bundle.
            :return: Execution dictionary with returncode, stdout, stderr.
            :exceptions: None.
        '''
        if not self._gui.is_initialized() or not service.is_initialized():
            return {
                'returncode': self.EXIT_FAILURE,
                'stdout': '',
                'stderr': (
                    'studio_command_executor::execute - '
                    'gui or service not initialized'
                ),
            }

        self._preloader.preload(params, self._gui)

        try:
            self._gui.start()
            return {
                'returncode': self.EXIT_SUCCESS,
                'stdout': 'botracked: studio session completed',
                'stderr': '',
            }
        except Exception as exc:
            return {
                'returncode': self.EXIT_FAILURE,
                'stdout': '',
                'stderr': f'studio_command_executor::execute - {exc}',
            }

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns definition metadata.

            :return: Command definition contract instance.
            :exceptions: None.
        '''
        return self._definition

    def __str__(self) -> str:
        '''
            Returns string representation of executor.

            :return: String.
            :exceptions: None.
        '''
        return to_str(self)
