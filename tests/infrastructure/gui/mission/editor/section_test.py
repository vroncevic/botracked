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
    Unit tests for MissionEditorSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.editor.section import MissionEditorSection
from botracked.infrastructure.gui.mission.syntax.highlighter.ihighlighter import IMissionSyntaxHighlighter

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionEditorSectionTest(TestCase):
    '''
        Tests MissionEditorSection buffer read/write and syntax refresh.
    '''

    @patch('botracked.infrastructure.gui.mission.editor.section.Scrollbar')
    @patch('botracked.infrastructure.gui.mission.editor.section.Text')
    @patch('botracked.infrastructure.gui.mission.editor.section.Frame')
    def test_editor_operations(
        self, frm_cls: MagicMock, txt_cls: MagicMock, _sb_cls: MagicMock
    ) -> None:
        '''
            Verifies get_script, set_script, and on_key_release highlighting.

            :param frm_cls: Patched Frame class.
            :param txt_cls: Patched Text class.
            :param _sb_cls: Patched Scrollbar class.
            :exceptions: None.
        '''
        txt_inst = MagicMock()
        txt_inst.get.return_value = 'STOP'
        txt_cls.return_value = txt_inst
        hl = MagicMock(spec=IMissionSyntaxHighlighter)

        sec = MissionEditorSection(MagicMock(spec=Frame), hl)
        self.assertIsInstance(sec, IMissionEditorSection)
        self.assertIs(sec.get_widget(), frm_cls.return_value)
        hl.setup_tags.assert_called_once_with(txt_inst)

        sec.set_script('FORWARD 500')
        txt_inst.insert.assert_called_once_with('1.0', 'FORWARD 500')
        self.assertEqual(sec.get_script(), 'STOP')

        sec.on_key_release(object())
        self.assertEqual(hl.apply_highlight.call_count, 2)


if __name__ == '__main__':
    main()
