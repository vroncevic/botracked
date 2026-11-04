# -*- coding: UTF-8 -*-

'''
Module
    repository.py
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
    Provides MissionPresetRepository filesystem adapter for .track presets.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from botracked.core.model.exceptions.preset_error import PresetError

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionPresetRepository:
    '''
        Defines class MissionPresetRepository implementing IMissionPresetRepository.
        Discovers and reads .track mission preset scripts from injected directory.

        It defines:

            :attributes:
                | DEFAULT_KEY - Fallback dictionary key when directory has no files.
                | DEFAULT_SCRIPT - Default fallback mission script text.
                | TRACK_GLOB - Filename glob pattern matching mission scripts.
                | ENCODING - Text file encoding used when reading .track scripts.
                | _presets_dir - Filesystem directory containing .track files.
            :methods:
                | __init__ - Initializes repository with presets directory path.
                | get_default_script - Returns baseline default mission script.
                | load_presets - Discovers and loads .track preset scripts.
                | __str__ - Returns string representation of repository adapter.
    '''

    DEFAULT_KEY: ClassVar[str] = 'default'
    DEFAULT_SCRIPT: ClassVar[str] = 'SPEED 160\nPING\nWAIT 0.5\nSTOP\n'
    TRACK_GLOB: ClassVar[str] = '*.track'
    ENCODING: ClassVar[str] = 'utf-8'

    _presets_dir: Path

    def __init__(self, presets_dir: Path) -> None:
        '''
            Initializes repository with presets directory path.

            :param presets_dir: Directory path scanned for .track scripts.
            :exceptions: None.
        '''
        self._presets_dir = presets_dir

    def get_default_script(self) -> str:
        '''
            Returns baseline default mission script.

            :return: Default .track script text.
            :exceptions: None.
        '''
        return self.DEFAULT_SCRIPT

    def load_presets(self) -> dict[str, str]:
        '''
            Discovers and loads .track preset scripts from configured directory.

            :return: Mapping of preset stem names to script source text.
            :exceptions:
                | PresetError: If an existing .track file cannot be decoded.
        '''
        discovered: dict[str, str] = {}

        if self._presets_dir.is_dir():
            for path in sorted(self._presets_dir.glob(self.TRACK_GLOB)):
                if path.is_file():
                    try:
                        discovered[path.stem] = path.read_text(
                            encoding=self.ENCODING
                        )

                    except (OSError, UnicodeDecodeError) as exc:
                        raise PresetError(
                            f'Failed to read preset {path.name}: {exc}'
                        ) from exc

        if not discovered:
            discovered[self.DEFAULT_KEY] = self.DEFAULT_SCRIPT

        return discovered

    def __str__(self) -> str:
        '''
            Returns string representation of repository adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
