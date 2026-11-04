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
    Defines BotGuiSessionFactory assembling the full Tkinter GUI session.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Frame, Style
from typing import ClassVar

from botracked.infrastructure.gui.console.dependencies import ConsolePanelDependencies
from botracked.infrastructure.gui.console.factory import ConsolePanelFactory
from botracked.infrastructure.gui.console.stream.dependencies import ConsoleStreamDependencies
from botracked.infrastructure.gui.console.stream.factory import ConsoleStreamFactory
from botracked.infrastructure.gui.console.toolbar.dependencies import ConsoleToolbarDependencies
from botracked.infrastructure.gui.console.toolbar.factory import ConsoleToolbarFactory
from botracked.infrastructure.gui.layout.bundle import GuiPanelsBundle
from botracked.infrastructure.gui.layout.dependencies import LayoutDependencies
from botracked.infrastructure.gui.layout.factory import LayoutFactory
from botracked.infrastructure.gui.lifecycle.dependencies import GuiLifecycleDependencies
from botracked.infrastructure.gui.lifecycle.factory import GuiLifecycleFactory
from botracked.infrastructure.gui.session.dependencies import GuiSessionDependencies
from botracked.infrastructure.gui.session.factory import GuiSessionFactory
from botracked.infrastructure.gui.session.isession import IGuiSession
from botracked.infrastructure.gui.theme.dependencies import ThemeDependencies
from botracked.infrastructure.gui.theme.factory import ThemeFactory
from botracked.infrastructure.gui.window.config import WindowConfig
from botracked.infrastructure.gui.window.dependencies import WindowDependencies
from botracked.infrastructure.gui.window.factory import WindowFactory
from botracked.setup.gui.cockpit.dependencies import CockpitDependencies
from botracked.setup.gui.cockpit.factory import CockpitFactory
from botracked.setup.gui.connection.dependencies import ConnectionDependencies
from botracked.setup.gui.connection.factory import ConnectionFactory
from botracked.setup.gui.dependencies import BotGuiSessionDependencies
from botracked.setup.gui.mission.dependencies import MissionDependencies
from botracked.setup.gui.mission.factory import MissionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotGuiSessionFactory:
    '''
        Defines class BotGuiSessionFactory assembling a mounted Tk GUI session.

        It defines:

            :attributes:
                | PANEL_STYLE - Panel ttk Frame style identifier.
                | CONSOLE_PADDING - Horizontal and vertical console padding.
            :methods:
                | create - Instantiates Tk root, panels, layout, and session.
                | get_version - Returns factory version string.
    '''

    PANEL_STYLE: ClassVar[str] = 'Panel.TFrame'
    CONSOLE_PADDING: ClassVar[tuple[int, int]] = (4, 4)

    @classmethod
    def create(cls, dependencies: BotGuiSessionDependencies) -> IGuiSession:
        '''
            Instantiates Tk root, mounts all cockpit panels, returns session.

            :param dependencies: GUI session collaborator ports bundle.
            :return: Assembled IGuiSession instance.
            :exceptions: None.
        '''
        root = Tk()
        window_prov = WindowFactory.create(
            WindowDependencies(
                root=root,
                style_configurator=ThemeFactory.create(
                    ThemeDependencies(style=Style(root))
                ).configurator,
                config=WindowConfig(),
            )
        )
        window_prov.configurator.configure()

        console_frame = Frame(
            root, style=cls.PANEL_STYLE, padding=cls.CONSOLE_PADDING
        )
        stream_prov = ConsoleStreamFactory.create(
            ConsoleStreamDependencies(parent=console_frame)
        )
        console_prov = ConsolePanelFactory.create(
            ConsolePanelDependencies(
                frame=console_frame,
                stream_section=stream_prov.section,
                toolbar_section=ConsoleToolbarFactory.create(
                    ConsoleToolbarDependencies(
                        parent=console_frame,
                        stream_section=stream_prov.section,
                    )
                ).section,
            )
        )
        layout_prov = LayoutFactory.create(LayoutDependencies(root=root))

        mission_panel = MissionFactory.create(
            MissionDependencies(
                parent=layout_prov.slots.mission_slot,
                dsl_service=dependencies.runtime.services.dsl,
                mission_runner=dependencies.runtime.runners.mission,
                preset_repository=dependencies.preset_repository,
                log_listener=console_prov.log_listener,
            )
        )
        cockpit = CockpitFactory.create(
            CockpitDependencies(
                root=root,
                parent=layout_prov.slots.cockpit_slot,
                services=dependencies.runtime.services,
                log_listener=console_prov.log_listener,
                packet_sink=console_prov.packet_sink,
            )
        )
        layout_prov.builder.mount_layout(
            layout_prov.slots,
            GuiPanelsBundle(
                connection=ConnectionFactory.create(
                    ConnectionDependencies(
                        root=root,
                        connection_service=(
                            dependencies.runtime.services.connection
                        ),
                        runners=dependencies.runtime.runners,
                        preferences_repository=(
                            dependencies.preferences_repository
                        ),
                        port_scanner=dependencies.port_scanner,
                        log_listener=console_prov.log_listener,
                    )
                ),
                mission=mission_panel,
                motion=cockpit.motion_panel,
                telemetry=cockpit.telemetry_panel,
                console=console_prov.panel,
            ),
        )
        lifecycle = GuiLifecycleFactory.create(
            GuiLifecycleDependencies(
                root=root,
                connection_service=dependencies.runtime.services.connection,
                listener=dependencies.runtime.runners.listener,
                poller=dependencies.runtime.runners.poller,
                mission_runner=dependencies.runtime.runners.mission,
            )
        )
        window_prov.configurator.bind_close_handler(lifecycle.runner)
        return GuiSessionFactory.create(
            GuiSessionDependencies(
                mission_panel=mission_panel,
                lifecycle_runner=lifecycle.runner,
            )
        ).session

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
