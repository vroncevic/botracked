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
from botracked.infrastructure.command.command import CommandBundle
from botracked.infrastructure.command.studio_command_definition import (
    StudioCommandDefinition,
)
from botracked.infrastructure.command.studio_command_executor import (
    StudioCommandExecutor,
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


class CLIBundleFactory:
    '''
        Factory constructing CLIBundle with registered commands and executors.

        It defines:

            :methods:
                | create_bundle - Creates and populates the CLI bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_bundle(
        cls, service: BotService, gui: BotrackedGUI, parser: IOptionManager
    ) -> CLIBundle:
        '''
            Creates the CLI bundle.

            :param service: BotService domain interactor.
            :type service: BotService

            :param gui: BotrackedGUI presentation adapter.
            :type gui: BotrackedGUI

            :param parser: OptionManager instance.
            :type parser: IOptionManager

            :return: Initialized CLIBundle.
            :rtype: CLIBundle

            :exceptions: None.
        '''
        studio_def = StudioCommandDefinition()
        studio_exec = StudioCommandExecutor(studio_def, gui)
        cmd_bundle = CommandBundle(definition=studio_def, executor=studio_exec)

        return CLIBundle(
            service=service,
            parser=parser,
            commands=[cmd_bundle],
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version.

            :return: Version string.
            :rtype: str

            :exceptions: None.
        '''
        return __version__
