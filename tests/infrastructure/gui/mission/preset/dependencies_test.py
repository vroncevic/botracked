# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for MissionPresetSectionDependencies.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.preset.dependencies import MissionPresetSectionDependencies
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPresetSectionDependenciesTest(TestCase):
    '''
        Tests MissionPresetSectionDependencies field retention.
    '''

    def test_fields(self) -> None:
        '''
            Verifies preset_repository and collaborator fields.

            :exceptions: None.
        '''
        repo = MagicMock(spec=IMissionPresetRepository)
        editor = MagicMock(spec=IMissionEditorSection)
        status = MagicMock(spec=IMissionStatusSection)
        deps = MissionPresetSectionDependencies(
            parent=MagicMock(spec=Frame),
            delegate=MagicMock(spec=IMissionActionDelegate),
            editor_section=editor,
            status_section=status,
            preset_repository=repo,
        )
        self.assertIs(deps.preset_repository, repo)
        self.assertIs(deps.editor_section, editor)
        self.assertIs(deps.status_section, status)


if __name__ == '__main__':
    main()
