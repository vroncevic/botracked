# -*- coding: UTF-8 -*-

'''
Module
    configurator.py
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
    Provides WindowConfigurator configuring root Tk application window.
'''

from __future__ import annotations

from tkinter import Tk
from typing import ClassVar

from botracked.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner
from botracked.infrastructure.gui.theme.colors import UIColors
from botracked.infrastructure.gui.theme.iconfigurator import IStyleConfigurator
from botracked.infrastructure.gui.window.config import WindowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class WindowConfigurator:
    '''
        Defines class WindowConfigurator implementing IWindowConfigurator.
        Configures top-level Tk window geometry, theme styling, and close protocol.

        It defines:

            :attributes:
                | DELETE_PROTOCOL - Window manager close protocol identifier.
                | _root - Root Tk window instance.
                | _style_configurator - Injected ttk style configurator port.
                | _config - Immutable WindowConfig window specification.
            :methods:
                | __init__ - Initializes configurator with root, style, and config.
                | configure - Applies title, geometry, background, and theme.
                | bind_close_handler - Binds shutdown handler to WM_DELETE_WINDOW.
    '''

    DELETE_PROTOCOL: ClassVar[str] = 'WM_DELETE_WINDOW'

    _root: Tk
    _style_configurator: IStyleConfigurator
    _config: WindowConfig

    def __init__(
        self,
        root: Tk,
        style_configurator: IStyleConfigurator,
        config: WindowConfig,
    ) -> None:
        '''
            Initializes window configurator with root window, style, and config.

            :param root: Root Tk window instance.
            :param style_configurator: Injected ttk style configurator contract.
            :param config: Immutable window dimensions and title specification.
            :exceptions: None.
        '''
        self._root = root
        self._style_configurator = style_configurator
        self._config = config

    def configure(self) -> None:
        '''
            Applies title, geometry, minimum size, background, and theme styling.

            :exceptions: None.
        '''
        self._root.title(self._config.window_title)
        self._root.geometry(
            f'{self._config.window_width}x{self._config.window_height}'
        )
        self._root.minsize(self._config.min_width, self._config.min_height)
        self._root.configure(background=UIColors.BG_DARK)
        self._root.option_add('*TCombobox*Listbox.background', UIColors.BG_SURFACE)
        self._root.option_add('*TCombobox*Listbox.foreground', UIColors.TEXT_MAIN)
        self._root.option_add('*TCombobox*Listbox.selectBackground', UIColors.BLUE)
        self._root.option_add('*TCombobox*Listbox.selectForeground', UIColors.BG_HEADER)
        self._style_configurator.apply()

    def bind_close_handler(self, runner: IGuiLifecycleRunner) -> None:
        '''
            Binds shutdown handler to WM_DELETE_WINDOW protocol.

            :param runner: Strongly-typed GUI lifecycle runner.
            :exceptions: None.
        '''
        self._root.protocol(self.DELETE_PROTOCOL, runner.stop)
