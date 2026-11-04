# -*- coding: UTF-8 -*-

'''
Module
    iconfigurator_test.py
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
    Unit tests for IWindowConfigurator protocol.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.theme.iconfigurator import IStyleConfigurator
from botracked.infrastructure.gui.window.config import WindowConfig
from botracked.infrastructure.gui.window.configurator import WindowConfigurator
from botracked.infrastructure.gui.window.iconfigurator import IWindowConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class IWindowConfiguratorTest(TestCase):
    '''
        Tests runtime structural conformance of IWindowConfigurator.
    '''

    def test_runtime_checkable(self) -> None:
        '''
            Verifies WindowConfigurator satisfies IWindowConfigurator.

            :exceptions: None.
        '''
        cfg = WindowConfigurator(
            root=MagicMock(spec=Tk),
            style_configurator=MagicMock(spec=IStyleConfigurator),
            config=WindowConfig(),
        )
        self.assertIsInstance(cfg, IWindowConfigurator)

if __name__ == '__main__':
    main()
