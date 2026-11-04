# -*- coding: UTF-8 -*-

'''
Module
    preloader_test.py
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
    Unit tests for ScriptPreloader.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.command.preloader import ScriptPreloader
from botracked.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ScriptPreloaderTest(TestCase):
    '''
        Tests ScriptPreloader path extraction and file loading.
    '''

    def test_preload_existing_and_missing_files(self) -> None:
        '''
            Verifies preloading valid .track file and rejecting missing paths.

            :exceptions: None.
        '''
        preloader = ScriptPreloader()
        gui = MagicMock(spec=IGUI)
        self.assertFalse(preloader.preload({}, gui))
        self.assertFalse(
            preloader.preload({'script': '/nonexistent/x.track'}, gui)
        )

        with TemporaryDirectory() as tmp_dir:
            track_path = Path(tmp_dir) / 'demo.track'
            track_path.write_text('PING\nSTOP\n', encoding='utf-8')
            loaded = preloader.preload({'script': str(track_path)}, gui)
            self.assertTrue(loaded)
            gui.load_script.assert_called_once_with('PING\nSTOP\n')

            with patch('builtins.open', side_effect=OSError('read error')):
                self.assertFalse(preloader.preload({'script': str(track_path)}, gui))

        self.assertTrue(str(preloader))


if __name__ == '__main__':
    main()
