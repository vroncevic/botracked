# -*- coding: UTF-8 -*-

'''
Module
    dsl_preset_loader.py
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
    Discovers and loads .track example presets from storage.
'''

from __future__ import annotations

from glob import glob
from os.path import abspath, basename, dirname, exists, isfile, join
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslPresetLoader:
    '''
        Defines class DslPresetLoader with attribute(s) and method(s).
        Discovers and loads .track mission preset scripts from disk.

        It defines:

            :attributes:
                | DEFAULT_SCRIPT - Default fallback mission script string.
            :methods:
                | get_default_script - Returns default fallback script.
                | load_presets - Discovers and loads preset scripts.
    '''

    DEFAULT_SCRIPT: ClassVar[str] = 'SPEED 160\nPING\nWAIT 0.5\nSTOP\n'

    @classmethod
    def get_default_script(cls) -> str:
        '''
            Returns default fallback .track script.

            :return: Script text.
            :exceptions: None.
        '''
        return cls.DEFAULT_SCRIPT

    @classmethod
    def load_presets(cls, search_dir: str | None = None) -> dict[str, str]:
        '''
            Discovers and loads .track example scripts from examples directory.

            :param search_dir: Optional custom examples directory path.
            :return: Mapping of preset names to script source text.
            :exceptions: None.
        '''
        discovered: dict[str, str] = {}
        target_dir: str = search_dir or join(
            dirname(dirname(dirname(dirname(dirname(abspath(__file__)))))),
            'examples',
        )

        if exists(target_dir):
            for path in sorted(glob(join(target_dir, '*.track'))):
                if isfile(path):
                    name: str = basename(path)[:-6]
                    try:
                        with open(path, 'r', encoding='utf-8') as fh:
                            discovered[name] = fh.read()
                    except (OSError, UnicodeDecodeError):
                        pass

        if not discovered:
            discovered['default'] = cls.DEFAULT_SCRIPT

        return discovered
