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
from typing import ClassVar

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.utils.reflection import to_str

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.setup.bundle import CLIBundle
from botracked.infrastructure.cli.setup.validator import CLIBundleValidator
from botracked.infrastructure.command.idefinition import ICommandDefinition
from botracked.infrastructure.command.iexecutor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLI:
    '''
        Inbound adapter for command line argument parsing and strategy dispatch.

        It defines:

            :attributes:
                | DEFAULT_COMMAND - Default subcommand executed when omitted.
                | EXIT_FAILURE - Error return code integer.
                | _service - Core robot application services bundle.
                | _parser - Option manager parser interface.
                | _executors - Mapping of command names to command executors.
                | _is_initialized - Flag tracking initialization state.
            :methods:
                | __init__ - Initializes CLI adapter with validated bundle.
                | is_initialized - Checks if CLI is initialized.
                | run - Parses CLI arguments and executes matching strategy.
                | __str__ - Returns string representation of CLI.
    '''

    DEFAULT_COMMAND: ClassVar[str] = 'studio'
    EXIT_FAILURE: ClassVar[int] = 1

    _service: BotRuntimeBundle
    _parser: IOptionManager
    _executors: Mapping[
        str,
        ICommandExecutor[
            ICommandDefinition,
            Mapping[str, object],
            Mapping[str, object],
            BotRuntimeBundle,
        ],
    ]
    _is_initialized: bool

    def __init__(self, bundle: CLIBundle) -> None:
        '''
            Initializes CLI adapter with validated bundle.

            :param bundle: CLIBundle instance.
            :exceptions:
                | ATSValueError: The CLI bundle must be provided and have proper values.
                | ATSTypeError:  The CLI bundle must be an instance of CLIBundle and
                |                its attributes must be instances of their respective types.
        '''
        CLIBundleValidator.validate(bundle)
        self._service = bundle.service
        self._parser = bundle.parser
        self._executors = {
            pair.definition.name: pair.executor for pair in bundle.commands
        }
        self._parser.register_commands(
            [pair.definition for pair in bundle.commands]
        )
        self._is_initialized = True

    def is_initialized(self) -> bool:
        '''
            Checks if CLI is initialized.

            :return: True if ready, False otherwise.
            :exceptions: None.
        '''
        return self._is_initialized

    def run(self) -> Mapping[str, object]:
        '''
            Parses CLI command arguments and executes matching command strategy.

            :return: Execution dictionary with returncode, stdout, stderr.
            :exceptions: None.
        '''
        try:
            command_name, params = self._parser.parse_command()

            if not command_name:
                command_name = self.DEFAULT_COMMAND

            if command_name in self._executors:
                return self._executors[command_name].execute(
                    params=params, service=self._service
                )

            return {
                'returncode': self.EXIT_FAILURE,
                'stdout': '',
                'stderr': f'botracked::cli: unknown command {command_name!r}',
            }

        except Exception as exc:
            return {
                'returncode': self.EXIT_FAILURE,
                'stdout': '',
                'stderr': f'botracked::cli exception: {exc}',
            }

    def __str__(self) -> str:
        '''
            Returns string representation of CLI.

            :return: String.
            :exceptions: None.
        '''
        return to_str(self)
