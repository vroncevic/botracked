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
    Defines MissionFactory assembling the mission routine studio panel.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from typing import ClassVar

from botracked.infrastructure.gui.mission.adapter.dependencies import MissionAdapterDependencies
from botracked.infrastructure.gui.mission.adapter.factory import MissionAdapterFactory
from botracked.infrastructure.gui.mission.dependencies import MissionPanelDependencies
from botracked.infrastructure.gui.mission.editor.dependencies import MissionEditorDependencies
from botracked.infrastructure.gui.mission.editor.factory import MissionEditorFactory
from botracked.infrastructure.gui.mission.factory import MissionPanelFactory
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.infrastructure.gui.mission.playback.dependencies import MissionPlaybackDependencies
from botracked.infrastructure.gui.mission.playback.factory import MissionPlaybackFactory
from botracked.infrastructure.gui.mission.preset.dependencies import MissionPresetSectionDependencies
from botracked.infrastructure.gui.mission.preset.factory import MissionPresetSectionFactory
from botracked.infrastructure.gui.mission.status.dependencies import MissionStatusDependencies
from botracked.infrastructure.gui.mission.status.factory import MissionStatusFactory
from botracked.infrastructure.gui.mission.syntax.config import MissionSyntaxConfig
from botracked.infrastructure.gui.mission.syntax.dependencies import MissionSyntaxDependencies
from botracked.infrastructure.gui.mission.syntax.factory import MissionSyntaxFactory
from botracked.infrastructure.gui.mission.toolbar.dependencies import MissionToolbarDependencies
from botracked.infrastructure.gui.mission.toolbar.factory import MissionToolbarFactory
from botracked.setup.gui.mission.dependencies import MissionDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionFactory:
    '''
        Defines class MissionFactory assembling mission studio panel.

        It defines:

            :attributes:
                | PANEL_STYLE - Panel ttk Frame style identifier.
                | PANEL_PADDING - Horizontal and vertical panel padding.
            :methods:
                | create - Wires and returns mounted IMissionPanel.
                | get_version - Returns factory version string.
    '''

    PANEL_STYLE: ClassVar[str] = 'Panel.TFrame'
    PANEL_PADDING: ClassVar[tuple[int, int]] = (8, 8)

    @classmethod
    def create(cls, dependencies: MissionDependencies) -> IMissionPanel:
        '''
            Wires mission adapter, syntax, editor, toolbar, and MissionPanel.

            :param dependencies: Mission GUI composition collaborators.
            :return: Assembled IMissionPanel instance.
            :exceptions: None.
        '''
        adapter_prov = MissionAdapterFactory.create(
            MissionAdapterDependencies(
                mission_runner=dependencies.mission_runner,
                dsl_service=dependencies.dsl_service,
                log_listener=dependencies.log_listener,
            )
        )
        syntax_prov = MissionSyntaxFactory.create(
            MissionSyntaxDependencies(config=MissionSyntaxConfig())
        )
        mission_frame = Frame(
            dependencies.parent,
            style=cls.PANEL_STYLE,
            padding=cls.PANEL_PADDING,
        )
        status_prov = MissionStatusFactory.create(
            MissionStatusDependencies(parent=mission_frame)
        )
        editor_prov = MissionEditorFactory.create(
            MissionEditorDependencies(
                parent=mission_frame,
                highlighter=syntax_prov.highlighter,
            )
        )
        toolbar_frame = Frame(mission_frame, style=cls.PANEL_STYLE)
        preset_prov = MissionPresetSectionFactory.create(
            MissionPresetSectionDependencies(
                parent=toolbar_frame,
                delegate=adapter_prov.delegate,
                editor_section=editor_prov.section,
                status_section=status_prov.section,
                preset_repository=dependencies.preset_repository,
            )
        )
        playback_prov = MissionPlaybackFactory.create(
            MissionPlaybackDependencies(
                parent=toolbar_frame,
                delegate=adapter_prov.delegate,
                editor_section=editor_prov.section,
                status_section=status_prov.section,
            )
        )
        toolbar_prov = MissionToolbarFactory.create(
            MissionToolbarDependencies(
                frame=toolbar_frame,
                preset_section=preset_prov.section,
                playback_section=playback_prov.section,
            )
        )
        return MissionPanelFactory.create(
            MissionPanelDependencies(
                frame=mission_frame,
                status_section=status_prov.section,
                editor_section=editor_prov.section,
                toolbar_section=toolbar_prov.section,
                initial_script=preset_prov.section.get_initial_script(),
            )
        ).panel

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
