# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for BotrackedBundleFactory.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from botracked.setup.bundle import BotrackedBundle
from botracked.setup.factory import BotrackedBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class BotrackedBundleFactoryTest(TestCase):
    '''
        Tests BotrackedBundleFactory headless system graph assembly.
    '''

    def test_create_bundle_default_and_with_options(self) -> None:
        '''
            Verifies default bundle creation and script preloading option.

            :exceptions: None.
        '''
        bundle = BotrackedBundleFactory.create_bundle()
        self.assertIsInstance(bundle, BotrackedBundle)
        self.assertTrue(bundle.gui.is_initialized())
        self.assertTrue(bundle.cli.is_initialized())
        self.assertEqual(BotrackedBundleFactory.get_version(), '1.0.2')

        with TemporaryDirectory() as tmp_dir:
            script_file = Path(tmp_dir) / 'init.track'
            script_file.write_text('PING\nSTOP\n', encoding='utf-8')
            opt_bundle = BotrackedBundleFactory.create_bundle_with_options(
                {'verbose': True, 'script': str(script_file)}
            )
            self.assertIsInstance(opt_bundle, BotrackedBundle)


if __name__ == '__main__':
    main()
