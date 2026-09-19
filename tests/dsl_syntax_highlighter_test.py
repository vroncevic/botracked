# -*- coding: UTF-8 -*-

'''
Module
    dsl_syntax_highlighter_test.py
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
    Unit tests for DslSyntaxHighlighter and DslSyntaxHighlighterConfig.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from tkinter import Tk, Text
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from botracked.infrastructure.gui.editor.dsl_syntax_highlighter import (
    DslSyntaxHighlighter,
)
from botracked.infrastructure.gui.editor.dsl_syntax_highlighter_config import (
    DslSyntaxHighlighterConfig,
)
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslSyntaxHighlighter(TestCase):
    '''
        Validates DslSyntaxHighlighter formatting and configuration behavior.
    '''

    _root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up headless Tkinter root instance.
        '''
        cls._root = Tk()
        cls._root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down Tkinter root instance.
        '''
        try:
            cls._root.destroy()
        except Exception:
            pass

    def test_config_defaults(self) -> None:
        '''
            Verifies default tag names, colors, and regexes.
        '''
        cfg = DslSyntaxHighlighterConfig()
        self.assertEqual(cfg.tag_keyword, 'keyword')
        self.assertEqual(cfg.tag_control, 'control')
        self.assertEqual(cfg.tag_number, 'number')
        self.assertEqual(cfg.tag_comment, 'comment')
        self.assertEqual(cfg.color_keyword, UIColors.CYAN)
        self.assertEqual(cfg.color_control, UIColors.GREEN)
        self.assertEqual(cfg.color_number, UIColors.AMBER)
        self.assertEqual(cfg.color_comment, UIColors.TEXT_MUTED)

    def test_setup_tags(self) -> None:
        '''
            Verifies tag setup on Text widget.
        '''
        highlighter = DslSyntaxHighlighter()
        text = Text(self._root)
        highlighter.setup_tags(text)
        tags = text.tag_names()
        self.assertIn('keyword', tags)
        self.assertIn('control', tags)
        self.assertIn('number', tags)
        self.assertIn('comment', tags)

    def test_apply_highlight_keywords_and_numbers(self) -> None:
        '''
            Verifies keyword and numeric literal tagging.
        '''
        highlighter = DslSyntaxHighlighter()
        text = Text(self._root)
        highlighter.setup_tags(text)
        text.insert('1.0', 'SPEED 160\nFORWARD 1.5\n')
        highlighter.apply_highlight(text)

        kw_ranges = text.tag_ranges('keyword')
        self.assertGreater(len(kw_ranges), 0)

        num_ranges = text.tag_ranges('number')
        self.assertGreater(len(num_ranges), 0)

    def test_apply_highlight_control_and_comment(self) -> None:
        '''
            Verifies control flow keyword and comment tagging.
        '''
        highlighter = DslSyntaxHighlighter()
        text = Text(self._root)
        highlighter.setup_tags(text)
        text.insert('1.0', 'REPEAT 4:\n# comment here\nEND\n')
        highlighter.apply_highlight(text)

        ctrl_ranges = text.tag_ranges('control')
        self.assertGreater(len(ctrl_ranges), 0)

        comment_ranges = text.tag_ranges('comment')
        self.assertGreater(len(comment_ranges), 0)

    def test_apply_highlight_comment_precedence(self) -> None:
        '''
            Verifies that comments take precedence over keyword recognition.
        '''
        highlighter = DslSyntaxHighlighter()
        text = Text(self._root)
        highlighter.setup_tags(text)
        text.insert('1.0', '# SPEED 200 FORWARD 2.0\n')
        highlighter.apply_highlight(text)

        kw_ranges = text.tag_ranges('keyword')
        self.assertEqual(len(kw_ranges), 0)

        comment_ranges = text.tag_ranges('comment')
        self.assertGreater(len(comment_ranges), 0)


if __name__ == '__main__':
    main()
