# -*- coding: UTF-8 -*-

'''
Module
    ihighlighter.py
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
    Defines IMissionSyntaxHighlighter protocol for full-buffer highlighting.
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
class IMissionSyntaxHighlighter(Protocol):
    '''
        Defines structural contract IMissionSyntaxHighlighter for DSL editor.

        It defines:

            :methods:
                | setup_tags - Configures color and font tags on Text widget.
                | apply_highlight - Clears old tags and highlights buffer lines.
    '''

    def setup_tags(self, text_widget: Text) -> None:
        '''
            Configures color and font tags on target Text widget.

            :param text_widget: Target Tkinter Text widget.
        '''

    def apply_highlight(self, text_widget: Text) -> None:
        '''
            Clears stale tags and applies syntax highlighting to buffer.

            :param text_widget: Target Tkinter Text widget.
        '''
