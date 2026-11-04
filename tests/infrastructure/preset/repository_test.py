# -*- coding: UTF-8 -*-

'''
Module
    repository_test.py
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
    Unit tests for MissionPresetRepository filesystem adapter.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from botracked.core.model.exceptions.preset_error import PresetError
from botracked.infrastructure.preset.repository import MissionPresetRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionPresetRepositoryTest(TestCase):
    '''
        Verifies MissionPresetRepository discovery, fallback, and PresetError.
    '''

    def test_missing_dir_returns_default_script(self) -> None:
        '''
            Verifies default fallback dictionary when directory does not exist.

            :exceptions: None.
        '''
        repo = MissionPresetRepository(Path('/nonexistent/botracked/presets'))
        self.assertEqual(
            repo.load_presets(), {'default': repo.get_default_script()}
        )
        self.assertIn('MissionPresetRepository', str(repo))

    def test_valid_and_corrupt_track_files(self) -> None:
        '''
            Verifies reading valid .track files and raising PresetError on bad UTF-8.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'patrol.track').write_text('PING\nSTOP\n', encoding='utf-8')
            repo = MissionPresetRepository(root)
            self.assertEqual(repo.load_presets(), {'patrol': 'PING\nSTOP\n'})

            (root / 'corrupt.track').write_bytes(b'\xff\xfe\xfd')
            with self.assertRaises(PresetError):
                repo.load_presets()


if __name__ == '__main__':
    main()
