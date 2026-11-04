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
    Unit tests for MissionToolbarDependencies.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.mission.playback.isection import IMissionPlaybackSection
from botracked.infrastructure.gui.mission.preset.isection import IMissionPresetSection
from botracked.infrastructure.gui.mission.toolbar.dependencies import MissionToolbarDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionToolbarDependenciesTest(TestCase):
    '''
        Tests MissionToolbarDependencies field retention.
    '''

    def test_fields(self) -> None:
        '''
            Verifies frame, preset_section, and playback_section fields.

            :exceptions: None.
        '''
        frame = MagicMock(spec=Frame)
        deps = MissionToolbarDependencies(
            frame=frame,
            preset_section=MagicMock(spec=IMissionPresetSection),
            playback_section=MagicMock(spec=IMissionPlaybackSection),
        )
        self.assertIs(deps.frame, frame)


if __name__ == '__main__':
    main()
