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
    Unit tests for PreferencesDependencies immutable bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from botracked.infrastructure.connection.preferences.dependencies import PreferencesDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferencesDependenciesTest(TestCase):
    '''
        Verifies PreferencesDependencies field storage and immutability.
    '''

    def test_bundle_creation_and_immutability(self) -> None:
        '''
            Verifies stored config_file, context_bundle, and frozen dataclass protection.

            :exceptions: None.
        '''
        path = Path('/tmp/connection.json')
        context: ContextBundle = ContextBundleFactory.create_bundle()
        deps = PreferencesDependencies(config_file=path, context_bundle=context)
        self.assertEqual(deps.config_file, path)
        self.assertEqual(deps.context_bundle, context)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'config_file', Path('/tmp/other.json'))


if __name__ == '__main__':
    main()
