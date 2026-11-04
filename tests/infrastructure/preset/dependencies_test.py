# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for PresetRepositoryDependencies immutable bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest import TestCase, main

from botracked.infrastructure.preset.dependencies import PresetRepositoryDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PresetRepositoryDependenciesTest(TestCase):
    '''
        Verifies PresetRepositoryDependencies path storage and immutability.
    '''

    def test_presets_dir_and_frozen(self) -> None:
        '''
            Verifies presets_dir storage and FrozenInstanceError on write.

            :exceptions: None.
        '''
        path = Path('/tmp/presets')
        deps = PresetRepositoryDependencies(presets_dir=path)
        self.assertEqual(deps.presets_dir, path)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'presets_dir', path)


if __name__ == '__main__':
    main()
