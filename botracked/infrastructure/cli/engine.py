# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines CLI class implementing inbound CLI port.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.utils.reflection import to_str

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.cli.setup.bundle import CLIBundle
from botracked.infrastructure.cli.setup.validator import CLIBundleValidator
from botracked.infrastructure.command.icommand_definition import (
    ICommandDefinition,
)
from botracked.infrastructure.command.icommand_executor import (
    ICommandExecutor,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLI:
    '''
        Inbound adapter for command line argument parsing and strategy dispatch.

        It defines:

            :attributes:
                | _service - Robot business service facade.
                | _parser - Option manager parser interface.
                | _executors - Mapping of command names to command executors.
                | _is_initialized - Flag tracking initialization state.
            :methods:
                | __init__ - Initializes CLI adapter with validated bundle.
                | is_initialized - Checks if CLI is initialized.
                | run - Parses CLI arguments and executes matching strategy.
                | __str__ - Returns string representation of CLI.
    '''

    _service: BotService
    _parser: IOptionManager
    _executors: Mapping[str, ICommandExecutor[ICommandDefinition, object, object, object]]
    _is_initialized: bool

    def __init__(self, bundle: CLIBundle) -> None:
        '''
            Initializes CLI adapter with validated bundle.

            :param bundle: CLIBundle instance.
            :type bundle: CLIBundle

            :return: None.
            :rtype: None

            :exceptions: None.
        '''
        CLIBundleValidator.validate(bundle)
        self._service = bundle.service
        self._parser = bundle.parser
        self._executors = {pair.definition.name: pair.executor for pair in bundle.commands}
        self._parser.register_commands([pair.definition for pair in bundle.commands])
        self._is_initialized = True

    def is_initialized(self) -> bool:
        '''
            Checks if CLI is initialized.

            :return: True if ready, False otherwise.
            :rtype: bool

            :exceptions: None.
        '''
        return self._is_initialized

    def run(self) -> Mapping[str, object]:
        '''
            Parses CLI command arguments and executes matching command strategy.

            :return: Execution dictionary with returncode, stdout, stderr.
            :rtype: Mapping[str, object]

            :exceptions: None.
        '''
        try:
            command_name, params = self._parser.parse_command()
            # If no command passed or default studio invoked:
            if not command_name:
                command_name = 'studio'

            executor = self._executors.get(command_name)
            if executor is not None:
                return executor.execute(params=params, service=self._service)

            return {
                'returncode': 1,
                'stdout': '',
                'stderr': f'botracked::cli: unknown command {command_name!r}',
            }
        except Exception as exc:
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': f'botracked::cli exception: {exc}',
            }

    def __str__(self) -> str:
        '''
            Returns string representation of CLI.

            :return: String.
            :rtype: str

            :exceptions: None.
        '''
        return to_str(self)
