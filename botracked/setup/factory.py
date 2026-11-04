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
from pathlib import Path
from typing import ClassVar

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.infrastructure.cli.dependencies import CLIDependencies
from botracked.infrastructure.cli.factory import CLIFactory
from botracked.infrastructure.cli.setup.factory import CLIBundleFactory
from botracked.infrastructure.cli.setup.options import CLIBundleOptions
from botracked.infrastructure.command.dependencies import CommandDependencies
from botracked.infrastructure.command.factory import CommandFactory
from botracked.infrastructure.command.preloader import ScriptPreloader
from botracked.infrastructure.connection.preferences.dependencies import PreferencesDependencies
from botracked.infrastructure.connection.preferences.factory import PreferencesFactory
from botracked.infrastructure.connection.scanner.dependencies import ScannerDependencies
from botracked.infrastructure.connection.scanner.factory import ScannerFactory
from botracked.infrastructure.gui.igui import IGUI
from botracked.infrastructure.preset.dependencies import PresetRepositoryDependencies
from botracked.infrastructure.preset.factory import PresetRepositoryFactory
from botracked.setup.bundle import BotrackedBundle
from botracked.setup.gui.dependencies import BotGuiSessionDependencies
from botracked.setup.gui.launcher import GuiSessionLauncher
from botracked.setup.keys import BotrackedBundleKeys
from botracked.setup.opt_validator import BotrackedBundleOptionsValidator
from botracked.setup.options import BotrackedBundleOptions
from botracked.setup.registry import BotrackedBundleRegistry
from botracked.setup.service.factory import BotServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleFactory:
    '''
        Factory assembling the complete dependency injection graph for botracked.

        It defines:

            :attributes:
                | DEFAULT_INFO_FILE - Default path to botracked.cfg info file.
                | DEFAULT_PRESETS_DIR - Repository examples directory for .track.
                | PREFS_DIR_NAME - User home hidden directory name.
                | PREFS_FILE_NAME - Connection preferences JSON filename.
                | SCANNER_INCLUDE_LINKS - Flag enabling symlink port scanning.
            :methods:
                | create_bundle - Constructs bundle with default options.
                | create_bundle_with_options - Constructs bundle with options.
                | get_version - Returns factory version string.
    '''

    DEFAULT_INFO_FILE: ClassVar[str] = join(
        dirname(dirname(abspath(__file__))),
        'infrastructure',
        'config',
        'botracked.cfg',
    )
    DEFAULT_PRESETS_DIR: ClassVar[Path] = (
        Path(__file__).resolve().parents[2] / 'examples'
    )
    PREFS_DIR_NAME: ClassVar[str] = '.botracked'
    PREFS_FILE_NAME: ClassVar[str] = 'preferences.json'
    SCANNER_INCLUDE_LINKS: ClassVar[bool] = False

    @classmethod
    def create_bundle(cls) -> BotrackedBundle:
        '''
            Constructs and wires all application components with default options.

            :return: Fully wired BotrackedBundle instance.
            :exceptions:
                | ATSValueError: If bundle validation fails.
                | ATSTypeError: If bundle component types are invalid.
        '''
        return cls.create_bundle_with_options(BotrackedBundleOptions())

    @classmethod
    def create_bundle_with_options(
        cls, options: BotrackedBundleOptions
    ) -> BotrackedBundle:
        '''
            Constructs and wires all application components with given options.

            :param options: Validated BotrackedBundleOptions mapping.
            :return: Fully wired BotrackedBundle instance.
            :exceptions:
                | ATSValueError: If bundle options or dependencies are invalid.
                | ATSTypeError: If bundle options or dependencies have bad types.
        '''
        BotrackedBundleOptionsValidator.validate(options)

        info_file: str = (
            options[BotrackedBundleKeys.OPTION_INFO_FILE]
            if BotrackedBundleKeys.OPTION_INFO_FILE in options
            else cls.DEFAULT_INFO_FILE
        )
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file,
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle(),
            )
        )
        service: BotRuntimeBundle = BotServiceFactory.create()
        prefs_repo = PreferencesFactory.create(
            PreferencesDependencies(
                config_file=(
                    Path.home() / cls.PREFS_DIR_NAME / cls.PREFS_FILE_NAME
                ),
                context_bundle=base_bundle.context_bundle,
            )
        ).repository
        scanner = ScannerFactory.create(
            ScannerDependencies(include_links=cls.SCANNER_INCLUDE_LINKS)
        ).scanner
        preset_repo = PresetRepositoryFactory.create(
            PresetRepositoryDependencies(presets_dir=cls.DEFAULT_PRESETS_DIR)
        ).repository

        gui: IGUI = GuiSessionLauncher(
            BotGuiSessionDependencies(
                runtime=service,
                preferences_repository=prefs_repo,
                port_scanner=scanner,
                preset_repository=preset_repo,
            )
        )
        cmd_prov = CommandFactory.create(CommandDependencies(gui=gui))
        if (
            BotrackedBundleKeys.OPTION_SCRIPT in options
            and options[BotrackedBundleKeys.OPTION_SCRIPT]
        ):
            cmd_prov.preloader.preload(
                {
                    ScriptPreloader.KEY_SCRIPT: options[
                        BotrackedBundleKeys.OPTION_SCRIPT
                    ]
                },
                gui,
            )

        cli = CLIFactory.create(
            CLIDependencies(
                bundle=CLIBundleFactory.create_bundle(
                    CLIBundleOptions(
                        service=service,
                        parser=base_bundle.option_manager,
                        commands=(cmd_prov.bundle,),
                    )
                )
            )
        ).cli

        return BotrackedBundleRegistry.create_bundle(
            {
                BotrackedBundleKeys.DEPENDENCY_BASE: base_bundle,
                BotrackedBundleKeys.DEPENDENCY_SERVICE: service,
                BotrackedBundleKeys.DEPENDENCY_GUI: gui,
                BotrackedBundleKeys.DEPENDENCY_CLI: cli,
            }
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
