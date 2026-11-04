# -*- coding: UTF-8 -*-

'''
Module
    section.py
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
    Provides MissionPresetSection leaf UI component for preset management.
'''

from __future__ import annotations

from tkinter import LEFT, StringVar
from tkinter.ttk import Button, Combobox, Frame, Label
from typing import ClassVar

from botracked.core.model.exceptions.preset_error import PresetError
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.preset.dependencies import MissionPresetSectionDependencies
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPresetSection:
    '''
        Defines class MissionPresetSection implementing IMissionPresetSection.
        Leaf UI section for selecting, loading, and validating .track presets.

        It defines:

            :attributes:
                | DEFAULT_KEY - Fallback key name when preset loading fails.
                | COMBO_EVENT - Tkinter virtual event for combobox selection.
                | COMBO_STATE - Readonly state string for preset Combobox.
                | COMBO_WIDTH - Character width of preset Combobox.
                | BTN_WIDTH - Action button character width.
                | WIDGET_PADX - Horizontal padding around child widgets.
                | _frame - Section container Frame widget.
                | _delegate - Mission action delegate port.
                | _editor_section - Mission editor leaf section port.
                | _status_section - Narrow mission status section port.
                | _preset_repo - Mission preset repository port.
                | _presets - Discovered mapping of preset names to scripts.
                | _preset_var - Bound StringVar tracking selected preset name.
            :methods:
                | __init__ - Initializes preset combobox and action buttons.
                | get_widget - Returns section container Frame widget.
                | get_initial_script - Returns initial preset script text.
                | on_load_selected - Loads selected preset into editor buffer.
                | on_preset_selected - Handles combobox selection event.
                | on_validate - Validates current editor script syntax.
    '''

    DEFAULT_KEY: ClassVar[str] = 'default'
    COMBO_EVENT: ClassVar[str] = '<<ComboboxSelected>>'
    COMBO_STATE: ClassVar[str] = 'readonly'
    COMBO_WIDTH: ClassVar[int] = 16
    BTN_WIDTH: ClassVar[int] = 0
    WIDGET_PADX: ClassVar[int] = 2

    _frame: Frame
    _delegate: IMissionActionDelegate
    _editor_section: IMissionEditorSection
    _status_section: IMissionStatusSection
    _preset_repo: IMissionPresetRepository
    _presets: dict[str, str]
    _preset_var: StringVar

    def __init__(self, dependencies: MissionPresetSectionDependencies) -> None:
        '''
            Initializes preset combobox and load/validate buttons.

            :param dependencies: Preset section collaborator ports bundle.
            :exceptions: None.
        '''
        self._frame = Frame(dependencies.parent, style='Panel.TFrame')
        self._delegate = dependencies.delegate
        self._editor_section = dependencies.editor_section
        self._status_section = dependencies.status_section
        self._preset_repo = dependencies.preset_repository

        try:
            self._presets = self._preset_repo.load_presets()
        except PresetError as exc:
            self._presets = {
                self.DEFAULT_KEY: self._preset_repo.get_default_script()
            }
            self._status_section.set_status(
                f'Preset error: {exc}', str(UIColors.AMBER)
            )

        names: tuple[str, ...] = tuple(self._presets.keys())
        first_name: str = names[0] if names else self.DEFAULT_KEY
        self._preset_var = StringVar(value=first_name)

        Label(
            self._frame, text='Preset:', style='Panel.TLabel'
        ).pack(side=LEFT, padx=self.WIDGET_PADX)

        combo = Combobox(
            self._frame,
            textvariable=self._preset_var,
            values=names,
            width=self.COMBO_WIDTH,
            state=self.COMBO_STATE,
        )
        combo.pack(side=LEFT, padx=self.WIDGET_PADX)
        combo.bind(self.COMBO_EVENT, self.on_preset_selected)

        Button(
            self._frame,
            text='Load',
            width=self.BTN_WIDTH,
            command=self.on_load_selected,
        ).pack(side=LEFT, padx=self.WIDGET_PADX)

        Button(
            self._frame,
            text='Validate',
            width=self.BTN_WIDTH,
            command=self.on_validate,
        ).pack(side=LEFT, padx=self.WIDGET_PADX)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_initial_script(self) -> str:
        '''
            Returns initial preset script for studio startup.

            :return: Initial .track script source text.
            :exceptions: None.
        '''
        selected: str = self._preset_var.get()
        if selected in self._presets:
            return self._presets[selected]
        return self._preset_repo.get_default_script()

    def on_load_selected(self) -> None:
        '''
            Loads currently selected preset into editor buffer.

            :exceptions: None.
        '''
        selected: str = self._preset_var.get()
        if selected in self._presets:
            self._editor_section.set_script(self._presets[selected])
            self._status_section.set_status(
                f'Loaded preset: {selected}', str(UIColors.CYAN)
            )

    def on_preset_selected(self, event: object) -> None:
        '''
            Handles combobox selection change event.

            :param event: Tkinter ComboboxSelected event object.
            :exceptions: None.
        '''
        _ = event
        self.on_load_selected()

    def on_validate(self) -> None:
        '''
            Validates current editor script syntax via mission delegate.

            :exceptions: None.
        '''
        script: str = self._editor_section.get_script()
        is_valid, message = self._delegate.handle_validate(script)
        fg_col: str = str(UIColors.GREEN if is_valid else UIColors.RED)
        self._status_section.set_status(message, fg_col)
