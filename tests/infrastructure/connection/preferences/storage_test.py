# -*- coding: UTF-8 -*-

'''
Module
    storage_test.py
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
    Unit tests for PreferencesStorage JSON file I/O adapter.
'''

from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase, main
from unittest.mock import patch

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.infrastructure.connection.preferences.storage import PreferencesStorage

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferencesStorageTest(TestCase):
    '''
        Verifies PreferencesStorage exists, read, write, and errors.
    '''

    _temp_dir: str
    _file_path: Path
    _context: ContextBundle
    _storage: PreferencesStorage

    def setUp(self) -> None:
        '''
            Creates isolated temporary directory and PreferencesStorage fixture.

            :exceptions: None.
        '''
        self._temp_dir = mkdtemp()
        self._file_path = Path(self._temp_dir) / 'nested' / 'connection.json'
        self._context = ContextBundleFactory.create_bundle()
        self._storage = PreferencesStorage(
            config_file=self._file_path,
            context_bundle=self._context,
        )

    def tearDown(self) -> None:
        '''
            Removes isolated temporary directory.

            :exceptions: None.
        '''
        rmtree(self._temp_dir)

    def test_write_read_and_str(self) -> None:
        '''
            Verifies full JSON write, read cycle, and str formatting.

            :exceptions: None.
        '''
        self.assertFalse(self._storage.exists())
        self._storage.write_payload({'port': '/dev/ttyUSB0', 'baud': 115200})
        self.assertTrue(self._storage.exists())
        self.assertEqual(
            self._storage.read_payload(),
            {'port': '/dev/ttyUSB0', 'baud': 115200},
        )
        self.assertIn('PreferencesStorage', str(self._storage))

    def test_read_missing_corrupted_or_non_dict_raises_error(self) -> None:
        '''
            Verifies missing file, invalid JSON, or JSON list raises error.

            :exceptions: None.
        '''
        with self.assertRaises(PreferencesError):
            self._storage.read_payload()

        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.write_text('{bad json', encoding='utf-8')
        with self.assertRaises(PreferencesError):
            self._storage.read_payload()

        self._file_path.write_text('[1, 2, 3]', encoding='utf-8')
        with self.assertRaises(PreferencesError):
            self._storage.read_payload()

        with patch('botracked.infrastructure.connection.preferences.storage.Loader.load_configuration', side_effect=OSError('io error')):
            with self.assertRaises(PreferencesError):
                self._storage.read_payload()

    def test_write_error_raises_preferences_error(self) -> None:
        '''
            Verifies write wraps TypeError/OSError or empty payload in PreferencesError.

            :exceptions: None.
        '''
        with self.assertRaises(PreferencesError):
            self._storage.write_payload({'bad': object()})

        with self.assertRaises(PreferencesError):
            self._storage.write_payload({})


if __name__ == '__main__':
    main()
