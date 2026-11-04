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
    Defines IMissionPresetSection protocol for preset selector leaf UI.
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
class IMissionPresetSection(Protocol):
    '''
        Defines structural contract IMissionPresetSection for preset controls.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | get_initial_script - Returns default or first preset script.
                | on_load_selected - Loads currently selected preset script.
                | on_preset_selected - Handles combobox selection event.
                | on_validate - Validates current editor script syntax.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def get_initial_script(self) -> str:
        '''
            Returns initial preset script for studio startup.

            :return: Initial .track script source text.
        '''

    def on_load_selected(self) -> None:
        '''
            Loads currently selected preset into editor buffer.
        '''

    def on_preset_selected(self, event: object) -> None:
        '''
            Handles combobox selection change event.

            :param event: Tkinter ComboboxSelected event object.
        '''

    def on_validate(self) -> None:
        '''
            Validates current editor script syntax via mission delegate.
        '''
