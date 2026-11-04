# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for MissionPresetSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.exceptions.preset_error import PresetError
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.preset.dependencies import MissionPresetSectionDependencies
from botracked.infrastructure.gui.mission.preset.isection import IMissionPresetSection
from botracked.infrastructure.gui.mission.preset.section import MissionPresetSection
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPresetSectionTest(TestCase):
    '''
        Tests MissionPresetSection preset loading, fallback, and validation.
    '''

    @patch('botracked.infrastructure.gui.mission.preset.section.Button')
    @patch('botracked.infrastructure.gui.mission.preset.section.Combobox')
    @patch('botracked.infrastructure.gui.mission.preset.section.Label')
    @patch('botracked.infrastructure.gui.mission.preset.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.preset.section.Frame')
    def test_preset_load_and_validate(self, *_mocks: MagicMock) -> None:
        '''
            Verifies preset selection, initial script, and validate dispatch.

            :param _mocks: Patched Tkinter widget and variable classes.
            :exceptions: None.
        '''
        frm_cls, svar_cls, _lbl, _cmb, _btn = _mocks
        pvar = MagicMock()
        pvar.get.return_value = 'square'
        svar_cls.return_value = pvar

        delegate = MagicMock(spec=IMissionActionDelegate)
        delegate.handle_validate.return_value = (True, 'Syntax OK')
        editor = MagicMock(spec=IMissionEditorSection)
        editor.get_script.return_value = 'STOP'
        status = MagicMock(spec=IMissionStatusSection)
        repo = MagicMock(spec=IMissionPresetRepository)
        repo.load_presets.return_value = {'square': 'FORWARD 1000\nSTOP'}
        repo.get_default_script.return_value = 'STOP'

        deps = MissionPresetSectionDependencies(
            parent=MagicMock(spec=Frame),
            delegate=delegate,
            editor_section=editor,
            status_section=status,
            preset_repository=repo,
        )
        sec = MissionPresetSection(deps)
        self.assertIsInstance(sec, IMissionPresetSection)
        self.assertIs(sec.get_widget(), frm_cls.return_value)
        self.assertEqual(sec.get_initial_script(), 'FORWARD 1000\nSTOP')

        sec.on_preset_selected(object())
        editor.set_script.assert_called_once_with('FORWARD 1000\nSTOP')

        pvar.get.return_value = 'missing'
        self.assertEqual(sec.get_initial_script(), 'STOP')

        sec.on_validate()
        delegate.handle_validate.assert_called_once_with('STOP')

    @patch('botracked.infrastructure.gui.mission.preset.section.Button')
    @patch('botracked.infrastructure.gui.mission.preset.section.Combobox')
    @patch('botracked.infrastructure.gui.mission.preset.section.Label')
    @patch('botracked.infrastructure.gui.mission.preset.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.preset.section.Frame')
    def test_preset_error_fallback(self, *_mocks: MagicMock) -> None:
        '''
            Verifies PresetError falls back cleanly to default script.

            :param _mocks: Patched Tkinter widget classes.
            :exceptions: None.
        '''
        status = MagicMock(spec=IMissionStatusSection)
        repo = MagicMock(spec=IMissionPresetRepository)
        repo.load_presets.side_effect = PresetError('bad dir')
        repo.get_default_script.return_value = 'STOP'
        deps = MissionPresetSectionDependencies(
            parent=MagicMock(spec=Frame),
            delegate=MagicMock(spec=IMissionActionDelegate),
            editor_section=MagicMock(spec=IMissionEditorSection),
            status_section=status,
            preset_repository=repo,
        )
        MissionPresetSection(deps)
        status.set_status.assert_called_once()


if __name__ == '__main__':
    main()
