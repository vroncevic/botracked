# -*- coding: UTF-8 -*-

'''
Module
    matcher_test.py
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
    Unit tests for MissionSyntaxMatcher.
'''

from __future__ import annotations

from tkinter import Text
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.mission.syntax.config import MissionSyntaxConfig
from botracked.infrastructure.gui.mission.syntax.matcher.matcher import MissionSyntaxMatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionSyntaxMatcherTest(TestCase):
    '''
        Tests MissionSyntaxMatcher regex tag spans for comments and commands.
    '''

    def test_highlight_comment_and_command_lines(self) -> None:
        '''
            Verifies comment line short-circuit and command/number tagging.

            :exceptions: None.
        '''
        cfg = MissionSyntaxConfig()
        matcher = MissionSyntaxMatcher(cfg)
        txt = MagicMock(spec=Text)

        matcher.highlight_line(txt, 1, '  # patrol header')
        txt.tag_add.assert_called_once_with('comment', '1.0', '1.17')

        txt.reset_mock()
        matcher.highlight_line(txt, 2, 'FORWARD 1000')
        self.assertGreaterEqual(txt.tag_add.call_count, 2)


if __name__ == '__main__':
    main()
