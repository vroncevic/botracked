# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines MissionPanelDependencies bundle for MissionPanelFactory.
'''

from __future__ import annotations

from dataclasses import dataclass
from tkinter.ttk import Frame

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

@dataclass(frozen=True, slots=True)
class MissionPanelDependencies:
    '''
        Immutable collaborator bundle injected into MissionPanelFactory.

        It defines:

            :attributes:
                | frame - Root container Frame widget.
                | status_section - Injected mission status leaf section port.
                | editor_section - Injected DSL editor leaf section port.
                | toolbar_section - Injected composite toolbar section port.
                | initial_script - Startup .track script text loaded into editor.
    '''

    frame: Frame
    status_section: IMissionStatusSection
    editor_section: IMissionEditorSection
    toolbar_section: IMissionToolbarSection
    initial_script: str
