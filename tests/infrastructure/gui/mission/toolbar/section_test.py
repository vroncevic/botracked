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
    Unit tests for MissionToolbarSection composite bar.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.mission.playback.isection import IMissionPlaybackSection
from botracked.infrastructure.gui.mission.preset.isection import IMissionPresetSection
from botracked.infrastructure.gui.mission.toolbar.isection import IMissionToolbarSection
from botracked.infrastructure.gui.mission.toolbar.section import MissionToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionToolbarSectionTest(TestCase):
    '''
        Tests MissionToolbarSection child section mounting and accessors.
    '''

    def test_toolbar_accessors(self) -> None:
        '''
            Verifies get_widget, get_preset_section, and get_playback_section.

            :exceptions: None.
        '''
        frame = MagicMock(spec=Frame)
        preset = MagicMock(spec=IMissionPresetSection)
        playback = MagicMock(spec=IMissionPlaybackSection)
        toolbar = MissionToolbarSection(frame, preset, playback)
        self.assertIsInstance(toolbar, IMissionToolbarSection)
        self.assertIs(toolbar.get_widget(), frame)
        self.assertIs(toolbar.get_preset_section(), preset)
        self.assertIs(toolbar.get_playback_section(), playback)


if __name__ == '__main__':
    main()
