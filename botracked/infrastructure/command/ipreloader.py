# -*- coding: UTF-8 -*-

'''
Module
    ipreloader.py
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
    Defines IScriptPreloader interface for preloading mission scripts from CLI.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScriptPreloader(Protocol):
    '''
        Defines protocol IScriptPreloader with method(s).
        Contract for extracting and preloading mission script files into GUI.

        It defines:

            :methods:
                | has_script_path - Checks whether CLI params designate a script path.
                | extract_script_path - Extracts script path string from CLI params.
                | preload - Reads designated script file and loads it into GUI.
    '''

    def has_script_path(self, params: Mapping[str, object]) -> bool:
        '''
            Checks whether CLI params designate a script path.

            :param params: Parameter mapping from CLI parser.
            :return: True if non-empty script path is present, False otherwise.
        '''

    def extract_script_path(self, params: Mapping[str, object]) -> str:
        '''
            Extracts script path string from CLI params.

            :param params: Parameter mapping from CLI parser.
            :return: Script path string or empty string when absent.
        '''

    def preload(self, params: Mapping[str, object], gui: IGUI) -> bool:
        '''
            Reads designated script file and loads it into GUI.

            :param params: Parameter mapping from CLI parser.
            :param gui: Target GUI presentation adapter.
            :return: True if script was preloaded, False otherwise.
        '''
