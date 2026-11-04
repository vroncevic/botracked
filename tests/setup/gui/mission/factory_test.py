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
    Unit tests for MissionFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.dsl.iservice import ITbotDslService
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.setup.gui.mission.dependencies import MissionDependencies
from botracked.setup.gui.mission.factory import MissionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionFactoryTest(TestCase):
    '''
        Tests MissionFactory headless assembly with mocked widgets.
    '''

    @patch('botracked.setup.gui.mission.factory.Frame')
    @patch('botracked.infrastructure.gui.mission.status.section.Frame')
    @patch('botracked.infrastructure.gui.mission.status.section.Label')
    @patch('botracked.infrastructure.gui.mission.status.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.editor.section.Frame')
    @patch('botracked.infrastructure.gui.mission.editor.section.Text')
    @patch('botracked.infrastructure.gui.mission.editor.section.Scrollbar')
    @patch('botracked.infrastructure.gui.mission.preset.section.Frame')
    @patch('botracked.infrastructure.gui.mission.preset.section.Label')
    @patch('botracked.infrastructure.gui.mission.preset.section.Combobox')
    @patch('botracked.infrastructure.gui.mission.preset.section.Button')
    @patch('botracked.infrastructure.gui.mission.preset.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.playback.section.Frame')
    @patch('botracked.infrastructure.gui.mission.playback.section.Button')
    @patch('botracked.infrastructure.gui.mission.panel.Label')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies MissionFactory wires IMissionPanel cleanly.

            :param _mocks: Patched Tkinter widget constructors.
            :exceptions: None.
        '''
        preset_repo = MagicMock(spec=IMissionPresetRepository)
        preset_repo.load_presets.return_value = {'01_ping': 'PING\n'}
        preset_repo.get_default_script.return_value = 'STOP\n'

        panel = MissionFactory.create(
            MissionDependencies(
                parent=MagicMock(spec=Tk),
                dsl_service=MagicMock(spec=ITbotDslService),
                mission_runner=MagicMock(spec=IMissionRunner),
                preset_repository=preset_repo,
                log_listener=MagicMock(spec=ILogListener),
            )
        )
        self.assertIsInstance(panel, IMissionPanel)
        self.assertEqual(MissionFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
