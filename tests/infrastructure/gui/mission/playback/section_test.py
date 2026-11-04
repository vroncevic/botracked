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
    Unit tests for MissionPlaybackSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.playback.dependencies import MissionPlaybackDependencies
from botracked.infrastructure.gui.mission.playback.isection import IMissionPlaybackSection
from botracked.infrastructure.gui.mission.playback.section import MissionPlaybackSection
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPlaybackSectionTest(TestCase):
    '''
        Tests MissionPlaybackSection Run, Pause, Resume, and Abort actions.
    '''

    @patch('botracked.infrastructure.gui.mission.playback.section.Button')
    @patch('botracked.infrastructure.gui.mission.playback.section.Frame')
    def test_playback_lifecycle_and_errors(
        self, frm_cls: MagicMock, _btn_cls: MagicMock
    ) -> None:
        '''
            Verifies run valid/invalid/error plus pause, resume, and abort.

            :param frm_cls: Patched Frame class.
            :param _btn_cls: Patched Button class.
            :exceptions: None.
        '''
        delegate = MagicMock(spec=IMissionActionDelegate)
        editor = MagicMock(spec=IMissionEditorSection)
        editor.get_script.return_value = 'FORWARD 500'
        status = MagicMock(spec=IMissionStatusSection)
        deps = MissionPlaybackDependencies(
            parent=MagicMock(spec=Frame),
            delegate=delegate,
            editor_section=editor,
            status_section=status,
        )
        sec = MissionPlaybackSection(deps)
        self.assertIsInstance(sec, IMissionPlaybackSection)
        self.assertIs(sec.get_widget(), frm_cls.return_value)

        delegate.handle_validate.return_value = (False, 'Syntax error')
        sec.on_run()
        delegate.handle_run.assert_not_called()

        delegate.handle_validate.return_value = (True, 'OK')
        sec.on_run()
        delegate.handle_run.assert_called_once_with('FORWARD 500')

        delegate.handle_run.side_effect = BotrackedError('link down')
        sec.on_run()

        sec.on_pause()
        delegate.handle_pause.assert_called_once()
        sec.on_resume()
        delegate.handle_resume.assert_called_once()
        sec.on_abort()
        delegate.handle_abort.assert_called_once()


if __name__ == '__main__':
    main()
