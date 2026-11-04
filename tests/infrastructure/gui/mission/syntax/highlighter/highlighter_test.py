# -*- coding: UTF-8 -*-

'''
Module
    highlighter_test.py
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
    Unit tests for MissionSyntaxHighlighter.
'''

from __future__ import annotations

from tkinter import Text
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.mission.syntax.config import MissionSyntaxConfig
from botracked.infrastructure.gui.mission.syntax.highlighter.highlighter import MissionSyntaxHighlighter
from botracked.infrastructure.gui.mission.syntax.matcher.imatcher import IMissionSyntaxMatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionSyntaxHighlighterTest(TestCase):
    '''
        Tests MissionSyntaxHighlighter tag setup and buffer pass.
    '''

    def test_setup_and_apply_highlight(self) -> None:
        '''
            Verifies setup_tags configures 4 tags and apply_highlight iterates lines.

            :exceptions: None.
        '''
        matcher = MagicMock(spec=IMissionSyntaxMatcher)
        hl = MissionSyntaxHighlighter(MissionSyntaxConfig(), matcher)
        txt = MagicMock(spec=Text)
        txt.get.return_value = '# title\nSTOP'
        hl.setup_tags(txt)
        self.assertEqual(txt.tag_configure.call_count, 4)
        hl.apply_highlight(txt)
        self.assertEqual(matcher.highlight_line.call_count, 2)


if __name__ == '__main__':
    main()
