# -*- coding: UTF-8 -*-

'''
Module
    dsl_editor_panel_config.py
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
    Provides DslEditorPanelConfig dataclass encapsulating DSL editor UI literals.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class DslEditorPanelConfig:
    '''
        Defines class DslEditorPanelConfig with attribute(s) and method(s).
        Immutable UI parameters, button labels, and defaults for DslEditorPanel.

        It defines:

            :attributes:
                | padding_main - Main container padding in pixels.
                | padding_bar - Action bar padding in pixels.
                | title_header - Panel header title text.
                | label_preset - Label text for preset dropdown.
                | btn_load - Label text for load button.
                | btn_validate - Label text for validate button.
                | btn_run - Label text for run mission button.
                | btn_pause - Label text for pause button.
                | btn_resume - Label text for resume button.
                | btn_abort - Label text for abort button.
                | default_status - Initial editor status message text.
                | font_family - Editor code font family name.
                | font_size - Editor code font size in points.
                | editor_height - Editor text area height in lines.
            :methods: None.
    '''

    padding_main: int = 8
    padding_bar: int = 4
    title_header: str = 'MISSION STUDIO (.track DSL)'
    label_preset: str = 'Preset:'
    btn_load: str = 'Load'
    btn_validate: str = 'Validate'
    btn_run: str = '▶ Run'
    btn_pause: str = '⏸ Pause'
    btn_resume: str = '⏯ Resume'
    btn_abort: str = '⏹ Abort'
    default_status: str = 'Ready. Author or select a preset .track routine.'
    font_family: str = 'Courier'
    font_size: int = 10
    editor_height: int = 6
