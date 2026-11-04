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
    Defines CommandFactory assembling studio command subsystem components.
'''

from __future__ import annotations

from botracked.infrastructure.command.bundle import CommandBundle
from botracked.infrastructure.command.definition import StudioCommandDefinition
from botracked.infrastructure.command.dependencies import CommandDependencies
from botracked.infrastructure.command.executor import StudioCommandExecutor
from botracked.infrastructure.command.preloader import ScriptPreloader
from botracked.infrastructure.command.provides import CommandProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFactory:
    '''
        Defines class CommandFactory assembling internal command components.

        It defines:

            :attributes: None.
            :methods:
                | create - Creates and wires CommandProvides bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: CommandDependencies) -> CommandProvides:
        '''
            Creates and wires studio command definition, preloader, and executor.

            :param dependencies: External command dependencies bundle.
            :return: Wired CommandProvides instance.
            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        preloader = ScriptPreloader()
        executor = StudioCommandExecutor(
            definition=definition,
            gui=dependencies.gui,
            preloader=preloader,
        )
        return CommandProvides(
            definition=definition,
            preloader=preloader,
            executor=executor,
            bundle=CommandBundle(definition=definition, executor=executor),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
