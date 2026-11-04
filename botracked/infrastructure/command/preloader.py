# -*- coding: UTF-8 -*-

'''
Module
    preloader.py
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
    Provides ScriptPreloader for loading script files into the GUI editor.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists, isfile
from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptPreloader:
    '''
        Defines class ScriptPreloader implementing IScriptPreloader structurally.
        Preloads mission script file into the GUI editor during startup.

        It defines:

            :attributes:
                | KEY_SCRIPT - Primary CLI parameter key for script path.
                | KEY_FILE - Secondary CLI parameter key for script path.
                | FILE_ENCODING - Text encoding for .track script files.
            :methods:
                | has_script_path - Checks whether CLI params designate a script path.
                | extract_script_path - Extracts script filepath from CLI params.
                | preload - Loads script content into GUI editor if designated.
                | __str__ - Returns string representation of preloader.
    '''

    KEY_SCRIPT: ClassVar[str] = 'script'
    KEY_FILE: ClassVar[str] = 'file'
    FILE_ENCODING: ClassVar[str] = 'utf-8'

    def has_script_path(self, params: Mapping[str, object]) -> bool:
        '''
            Checks whether CLI params designate a script path.

            :param params: Parameter dictionary from CLI parsing.
            :return: True if non-empty script path is present, False otherwise.
            :exceptions: None.
        '''
        return bool(self.extract_script_path(params))

    def extract_script_path(self, params: Mapping[str, object]) -> str:
        '''
            Extracts script filepath from CLI parameter mapping.

            :param params: Parameter dictionary from CLI parsing.
            :return: Filepath string if present, empty string otherwise.
            :exceptions: None.
        '''
        for key in (self.KEY_SCRIPT, self.KEY_FILE):
            candidate: object = params.get(key, '')
            if isinstance(candidate, str) and candidate.strip():
                return candidate
        return ''

    def preload(self, params: Mapping[str, object], gui: IGUI) -> bool:
        '''
            Loads script content into GUI editor if designated.

            :param params: Parameter dictionary from CLI parsing.
            :param gui: GUI adapter instance.
            :return: True if script was preloaded, False otherwise.
            :exceptions: None.
        '''
        if not self.has_script_path(params):
            return False
        script_path: str = self.extract_script_path(params)
        if not exists(script_path) or not isfile(script_path):
            return False
        try:
            with open(script_path, 'r', encoding=self.FILE_ENCODING) as script_file:
                content: str = script_file.read()
        except (OSError, UnicodeDecodeError):
            return False
        gui.load_script(content)
        return True

    def __str__(self) -> str:
        '''
            Returns string representation of preloader.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
