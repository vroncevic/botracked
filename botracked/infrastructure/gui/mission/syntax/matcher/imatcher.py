# -*- coding: UTF-8 -*-

'''
Module
    imatcher.py
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
    Defines IMissionSyntaxMatcher protocol for line-level regex tagging.
'''

from __future__ import annotations

from tkinter import Text
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMissionSyntaxMatcher(Protocol):
    '''
        Defines structural contract IMissionSyntaxMatcher for line regex tagging.

        It defines:

            :methods:
                | match_and_tag - Applies regex tag across a single editor line.
                | highlight_line - Highlights comments, keywords, and numbers.
    '''

    def match_and_tag(
        self,
        text_widget: Text,
        pattern_str: str,
        tag_name: str,
        line_spec: tuple[int, str],
    ) -> None:
        '''
            Applies regex pattern tag across a single editor line.

            :param text_widget: Target Tkinter Text widget.
            :param pattern_str: Regular expression pattern string.
            :param tag_name: Tag identifier to apply on matches.
            :param line_spec: Tuple of 1-based line index and line text.
        '''

    def highlight_line(
        self, text_widget: Text, line_idx: int, line_content: str
    ) -> None:
        '''
            Highlights comments, keywords, control blocks, and numbers on line.

            :param text_widget: Target Tkinter Text widget.
            :param line_idx: 1-based line number in Text widget.
            :param line_content: Raw string content of target line.
        '''
