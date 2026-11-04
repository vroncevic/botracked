# -*- coding: UTF-8 -*-

'''
Module
    configurator_test.py
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
    Unit tests for WindowConfigurator.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from botracked.infrastructure.gui.theme.iconfigurator import IStyleConfigurator
from botracked.infrastructure.gui.window.config import WindowConfig
from botracked.infrastructure.gui.window.configurator import WindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class WindowConfiguratorTest(TestCase):
    '''
        Tests WindowConfigurator root window setup and WM_DELETE_WINDOW bind.
    '''

    def test_configure_and_bind_close_handler(self) -> None:
        '''
            Verifies title, geometry, style apply, and close handler binding.

            :exceptions: None.
        '''
        root = MagicMock(spec=Tk)
        style_cfg = MagicMock(spec=IStyleConfigurator)
        configurator = WindowConfigurator(
            root=root, style_configurator=style_cfg, config=WindowConfig()
        )
        configurator.configure()
        root.title.assert_called_once()
        style_cfg.apply.assert_called_once()

        runner = MagicMock(spec=IGuiLifecycleRunner)
        configurator.bind_close_handler(runner)
        root.protocol.assert_called_once_with('WM_DELETE_WINDOW', runner.stop)

if __name__ == '__main__':
    main()
