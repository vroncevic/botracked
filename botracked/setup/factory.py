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
    Factory constructing the BotrackedBundle and assembling system layers.
'''

from __future__ import annotations

from os.path import abspath, dirname, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from botracked.core.service.bot_service import BotService
from botracked.infrastructure.cli.engine import CLI
from botracked.infrastructure.cli.setup.bundle import CLIBundle
from botracked.infrastructure.cli.setup.factory import CLIBundleFactory
from botracked.infrastructure.cli.setup.options import CLIBundleOptions
from botracked.infrastructure.gui.engine import BotrackedGUI
from botracked.setup.bundle import BotrackedBundle
from botracked.setup.dependencies import BotrackedBundleDependencies
from botracked.setup.keys import BotrackedBundleKeys
from botracked.setup.opt_validator import BotrackedBundleOptionsValidator
from botracked.setup.options import BotrackedBundleOptions
from botracked.setup.registry import BotrackedBundleRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotrackedBundleFactory:
    '''
        Factory assembling the complete dependency injection graph for botracked.

        It defines:

            :attributes:
                | _info_file - Default path to botracked.cfg configuration file.
            :methods:
                | create_bundle - Constructs and wires all components.
                | get_version - Returns factory version string.
    '''

    _info_file: str = join(dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'botracked.cfg',)

    @classmethod
    def create_bundle(cls, options: BotrackedBundleOptions | None = None) -> BotrackedBundle:
        '''
            Constructs and wires all application components.

            :param options: Optional pre-configured bundle options.
            :return: Fully wired BotrackedBundle instance.
            :exceptions:
                | ATSValueError: The botracked bundle options must be provided and have proper values.
                | ATSTypeError:  The botracked bundle options must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The botracked bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The botracked bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The botracked bundle must be provided and have proper values.
                | ATSTypeError:  The botracked bundle must be an instance of BotrackedBundle and
                |                its attributes must be instances of their respective types.
        '''
        if options is not None:
            BotrackedBundleOptionsValidator.validate(options)

        info_file: str = (
            options[BotrackedBundleKeys.OPTION_INFO_FILE]
            if options is not None and BotrackedBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        context_bundle: ContextBundle = ContextBundleFactory.create_bundle()
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=context_bundle,
            )
        )

        service: BotService = BotService()
        gui: BotrackedGUI = BotrackedGUI(bot_service=service)

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            CLIBundleOptions(
                service=service,
                gui=gui,
                parser=base_bundle.option_manager,
            )
        )
        cli: CLI = CLI(cli_bundle)

        dependencies: BotrackedBundleDependencies = {
            BotrackedBundleKeys.DEPENDENCY_BASE: base_bundle,
            BotrackedBundleKeys.DEPENDENCY_SERVICE: service,
            BotrackedBundleKeys.DEPENDENCY_GUI: gui,
            BotrackedBundleKeys.DEPENDENCY_CLI: cli,
        }

        return BotrackedBundleRegistry.create_bundle(dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
