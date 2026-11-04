# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Provides MissionPanel composite UI component for mission routine studio.
'''

from __future__ import annotations

from tkinter import BOTH, BOTTOM, TOP, X
from tkinter.ttk import Frame, Label
from typing import ClassVar

from botracked.infrastructure.gui.mission.dependencies import MissionPanelDependencies
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection
from botracked.infrastructure.gui.mission.toolbar.isection import IMissionToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPanel:
    '''
        Defines class MissionPanel implementing IMissionPanel contract.
        Composite studio panel mounting toolbar, DSL editor, and status bar.

        It defines:

            :attributes:
                | HEADER_TEXT - Panel title caption.
                | SECTION_GAP - Vertical spacing between child sections.
                | _frame - Root container Frame widget.
                | _status_section - Injected status indicator section port.
                | _editor_section - Injected DSL editor section port.
                | _toolbar_section - Injected composite toolbar section port.
            :methods:
                | __init__ - Mounts injected sections and loads initial script.
                | get_widget - Returns root container Frame widget.
                | get_script - Returns current DSL script text from editor.
                | set_script - Replaces editor DSL script text.
                | set_status - Updates mission status indicator caption.
                | get_status_text - Returns current mission status caption.
    '''

    HEADER_TEXT: ClassVar[str] = 'MISSION ROUTINE STUDIO (.track DSL)'
    SECTION_GAP: ClassVar[int] = 6

    _frame: Frame
    _status_section: IMissionStatusSection
    _editor_section: IMissionEditorSection
    _toolbar_section: IMissionToolbarSection

    def __init__(self, dependencies: MissionPanelDependencies) -> None:
        '''
            Mounts injected sections and populates initial script buffer.

            :param dependencies: Mission panel collaborator ports bundle.
            :exceptions: None.
        '''
        self._frame = dependencies.frame
        self._status_section = dependencies.status_section
        self._editor_section = dependencies.editor_section
        self._toolbar_section = dependencies.toolbar_section

        Label(
            self._frame,
            text=self.HEADER_TEXT,
            style='PanelHeader.TLabel',
        ).pack(side=TOP, anchor='w', pady=(0, self.SECTION_GAP))

        self._toolbar_section.get_widget().pack(
            in_=self._frame, fill=X, side=TOP, pady=(0, self.SECTION_GAP)
        )
        self._status_section.get_widget().pack(
            in_=self._frame, fill=X, side=BOTTOM, pady=(self.SECTION_GAP, 0)
        )
        self._editor_section.get_widget().pack(
            in_=self._frame, fill=BOTH, expand=True
        )

        if dependencies.initial_script:
            self._editor_section.set_script(dependencies.initial_script)

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Root Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_script(self) -> str:
        '''
            Returns current DSL script text from editor.

            :return: Raw .track script string.
            :exceptions: None.
        '''
        return self._editor_section.get_script()

    def set_script(self, script: str) -> None:
        '''
            Replaces editor DSL script text.

            :param script: Raw .track script string.
            :exceptions: None.
        '''
        self._editor_section.set_script(script)

    def set_status(self, message: str, fg_color: str) -> None:
        '''
            Updates mission status indicator caption and foreground color.

            :param message: Status message text.
            :param fg_color: Foreground color hex string.
            :exceptions: None.
        '''
        self._status_section.set_status(message, fg_color)

    def get_status_text(self) -> str:
        '''
            Returns current mission status indicator text.

            :return: Status caption string.
            :exceptions: None.
        '''
        return self._status_section.get_status_text()
