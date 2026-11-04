# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for MissionPresetSectionFactory.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.preset.dependencies import MissionPresetSectionDependencies
from botracked.infrastructure.gui.mission.preset.factory import MissionPresetSectionFactory
from botracked.infrastructure.gui.mission.preset.isection import IMissionPresetSection
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPresetSectionFactoryTest(TestCase):
    '''
        Tests MissionPresetSectionFactory assembly and version string.
    '''

    @patch('botracked.infrastructure.gui.mission.preset.section.Button')
    @patch('botracked.infrastructure.gui.mission.preset.section.Combobox')
    @patch('botracked.infrastructure.gui.mission.preset.section.Label')
    @patch('botracked.infrastructure.gui.mission.preset.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.preset.section.Frame')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies create produces MissionPresetSectionProvides and version 1.0.2.

            :param _mocks: Patched Tkinter widget classes.
            :exceptions: None.
        '''
        repo = MagicMock(spec=IMissionPresetRepository)
        repo.load_presets.return_value = {'patrol': 'STOP'}
        deps = MissionPresetSectionDependencies(
            parent=MagicMock(spec=Frame),
            delegate=MagicMock(spec=IMissionActionDelegate),
            editor_section=MagicMock(spec=IMissionEditorSection),
            status_section=MagicMock(spec=IMissionStatusSection),
            preset_repository=repo,
        )
        provides = MissionPresetSectionFactory.create(deps)
        self.assertIsInstance(provides.section, IMissionPresetSection)
        self.assertEqual(MissionPresetSectionFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
