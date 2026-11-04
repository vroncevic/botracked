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
    Unit tests for MissionStatusSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection
from botracked.infrastructure.gui.mission.status.section import MissionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionStatusSectionTest(TestCase):
    '''
        Tests MissionStatusSection status caption and color updates.
    '''

    @patch('botracked.infrastructure.gui.mission.status.section.Label')
    @patch('botracked.infrastructure.gui.mission.status.section.StringVar')
    @patch('botracked.infrastructure.gui.mission.status.section.Frame')
    def test_status_update(
        self, frm_cls: MagicMock, svar_cls: MagicMock, lbl_cls: MagicMock
    ) -> None:
        '''
            Verifies set_status and get_status_text on MissionStatusSection.

            :param frm_cls: Patched Frame class.
            :param svar_cls: Patched StringVar class.
            :param lbl_cls: Patched Label class.
            :exceptions: None.
        '''
        svar = MagicMock()
        svar.get.return_value = 'Validated OK'
        svar_cls.return_value = svar
        sec = MissionStatusSection(MagicMock(spec=Frame))
        self.assertIsInstance(sec, IMissionStatusSection)
        self.assertIs(sec.get_widget(), frm_cls.return_value)
        sec.set_status('Validated OK', '#00FF88')
        svar.set.assert_called_once_with('Validated OK')
        lbl_cls.return_value.configure.assert_called_once_with(foreground='#00FF88')
        self.assertEqual(sec.get_status_text(), 'Validated OK')


if __name__ == '__main__':
    main()
