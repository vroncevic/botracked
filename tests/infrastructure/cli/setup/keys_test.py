# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
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
    Unit tests for CLIBundleKeys.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.infrastructure.cli.setup.keys import CLIBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class CLIBundleKeysTest(TestCase):
    '''
        Tests CLIBundleKeys constants and MappingProxyType outputs.
    '''

    def test_keys_and_type_mappings(self) -> None:
        '''
            Verifies dependency and option key names and type proxies.

            :exceptions: None.
        '''
        dep_map = CLIBundleKeys.get_dependency_to_type()
        opt_map = CLIBundleKeys.get_option_to_type()
        self.assertIn(CLIBundleKeys.DEPENDENCY_COMMANDS, dep_map)
        self.assertIn(CLIBundleKeys.OPTION_COMMANDS, opt_map)


if __name__ == '__main__':
    main()
