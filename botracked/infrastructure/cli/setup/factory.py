# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for creating the CLIBundle.
'''

from __future__ import annotations

from ats_utilities.option.imanager import IOptionManager

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.cli.setup.bundle import CLIBundle
from botracked.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from botracked.infrastructure.cli.setup.keys import CLIBundleKeys
from botracked.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from botracked.infrastructure.cli.setup.options import CLIBundleOptions
from botracked.infrastructure.cli.setup.registry import CLIBundleRegistry
from botracked.infrastructure.command.command import CommandBundle
from botracked.infrastructure.command.studio_command_definition import StudioCommandDefinition
from botracked.infrastructure.command.studio_command_executor import StudioCommandExecutor
from botracked.infrastructure.gui.engine import BotrackedGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleFactory:
    '''
        Factory constructing CLIBundle with registered commands and executors.

        It defines:

            :methods:
                | create_bundle - Creates and populates the CLI bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_bundle(cls, options: CLIBundleOptions) -> CLIBundle:
        '''
            Creates the CLI bundle with configured options.

            :param options: The CLI bundle options.
            :return: The assembled CLIBundle instance.
            :exceptions:
                | ATSValueError: The cli bundle options must be provided and have proper values.
                | ATSTypeError:  The cli bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The cli bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The cli bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The cli bundle must be provided and have proper values.
                | ATSTypeError:  The cli bundle must be an instance of CLIBundle and
                |                its attributes must be instances of their respective types.
        '''
        CLIBundleOptionsValidator.validate(options)

        service: BotService = options[CLIBundleKeys.OPTION_SERVICE]
        gui: BotrackedGUI = options[CLIBundleKeys.OPTION_GUI]
        parser: IOptionManager = options[CLIBundleKeys.OPTION_PARSER]

        studio_def: StudioCommandDefinition = StudioCommandDefinition()
        studio_exec: StudioCommandExecutor = StudioCommandExecutor(studio_def, gui)
        cmd_bundle: CommandBundle = CommandBundle(
            definition=studio_def, executor=studio_exec
        )

        dependencies: CLIBundleDependencies = {
            CLIBundleKeys.DEPENDENCY_SERVICE: service,
            CLIBundleKeys.DEPENDENCY_PARSER: parser,
            CLIBundleKeys.DEPENDENCY_COMMANDS: [cmd_bundle],
        }

        return CLIBundleRegistry.create_bundle(dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
