# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Encapsulates core botracked components for simplification of botracked bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from botracked.core.service.ibot_service import IBotService
from botracked.infrastructure.cli.icli import ICLI
from botracked.infrastructure.gui.igui import IGUI
from botracked.setup.bundle import BotrackedBundle
from botracked.setup.dependencies import BotrackedBundleDependencies
from botracked.setup.dep_validator import BotrackedBundleDependenciesValidator
from botracked.setup.keys import BotrackedBundleKeys
from botracked.setup.validator import BotrackedBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotrackedBundleRegistry:
    '''
        Encapsulates core botracked components for simplification of botracked
        bundle.

        It defines:

            :methods:
                | create_bundle - Creates the botracked bundle from dependencies.
                | get_version - Returns the registry version string.
    '''

    @classmethod
    def create_bundle(cls, dependencies: BotrackedBundleDependencies) -> BotrackedBundle:
        '''
            Creates the botracked bundle from validated dependencies.

            :param dependencies: The botracked bundle dependencies.
            :type dependencies: BotrackedBundleDependencies

            :return: The assembled BotrackedBundle.
            :rtype: BotrackedBundle

            :exceptions: None.
        '''
        BotrackedBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle = dependencies[BotrackedBundleKeys.DEPENDENCY_BASE]
        service: IBotService = dependencies[BotrackedBundleKeys.DEPENDENCY_SERVICE]
        gui: IGUI = dependencies[BotrackedBundleKeys.DEPENDENCY_GUI]
        cli: ICLI = dependencies[BotrackedBundleKeys.DEPENDENCY_CLI]

        bundle: BotrackedBundle = BotrackedBundle(
            base=base,
            service=service,
            gui=gui,
            cli=cli,
        )
        BotrackedBundleValidator.validate(bundle)
        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: Version string.
            :rtype: str

            :exceptions: None.
        '''
        return __version__
