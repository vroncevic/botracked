# -*- coding: UTF-8 -*-

'''
Module
    isection.py
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
    Defines IMissionEditorSection protocol for DSL script editor leaf UI.
'''

from __future__ import annotations

from tkinter.ttk import Frame
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
class IMissionEditorSection(Protocol):
    '''
        Defines structural contract IMissionEditorSection for DSL code editor.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | get_script - Returns raw script text from editor buffer.
                | set_script - Replaces editor buffer and applies highlighting.
                | on_key_release - Re-highlights buffer on editor key release.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def get_script(self) -> str:
        '''
            Returns raw script text from editor buffer.

            :return: Raw .track script string.
        '''

    def set_script(self, text: str) -> None:
        '''
            Replaces editor buffer and applies syntax highlighting.

            :param text: Raw .track script string.
        '''

    def on_key_release(self, event: object) -> None:
        '''
            Re-highlights buffer on editor key release event.

            :param event: Tkinter KeyRelease event object.
        '''
