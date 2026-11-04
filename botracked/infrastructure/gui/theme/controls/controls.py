# -*- coding: UTF-8 -*-

'''
Module
    controls.py
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
    Provides ControlStyleConfigurator styling combobox, scale, and scrollbar.
'''

from __future__ import annotations

from tkinter.ttk import Style

from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ControlStyleConfigurator:
    '''
        Defines class ControlStyleConfigurator implementing
        IControlStyleConfigurator contract structurally.

        It defines:

            :attributes:
                | _style - Bound ttk Style manager instance.
            :methods:
                | __init__ - Initializes configurator with ttk Style manager.
                | apply - Applies dark cockpit styles to interactive controls.
                | configure_combobox - Configures dark combobox field and states.
                | configure_bars - Configures dark scale and scrollbar styles.
    '''

    _style: Style

    def __init__(self, style: Style) -> None:
        '''
            Initializes configurator with ttk Style manager.

            :param style: Tkinter ttk Style instance.
            :exceptions: None.
        '''
        self._style = style

    def apply(self) -> None:
        '''
            Applies dark cockpit styles to interactive ttk controls.

            :exceptions: None.
        '''
        self.configure_combobox()
        self.configure_bars()

    def configure_combobox(self) -> None:
        '''
            Configures dark combobox field, arrow, and state mappings.

            :exceptions: None.
        '''
        self._style.configure(
            'TCombobox',
            fieldbackground=UIColors.BG_DARK,
            background=UIColors.BG_SURFACE,
            foreground=UIColors.TEXT_MAIN,
            arrowcolor=UIColors.CYAN,
            bordercolor=UIColors.BORDER,
            lightcolor=UIColors.BG_SURFACE,
            darkcolor=UIColors.BG_DARK,
            selectbackground=UIColors.BLUE,
            selectforeground=UIColors.BG_HEADER,
            insertcolor=UIColors.CYAN,
        )
        self._style.map(
            'TCombobox',
            fieldbackground=[
                ('readonly', UIColors.BG_DARK),
                ('disabled', UIColors.BG_PANEL),
                ('!disabled', UIColors.BG_DARK),
            ],
            foreground=[
                ('readonly', UIColors.TEXT_MAIN),
                ('disabled', UIColors.TEXT_DIM),
                ('!disabled', UIColors.TEXT_MAIN),
            ],
            background=[
                ('active', UIColors.BORDER),
                ('!disabled', UIColors.BG_SURFACE),
            ],
            selectbackground=[('readonly', UIColors.BG_DARK)],
            selectforeground=[('readonly', UIColors.TEXT_MAIN)],
        )

    def configure_bars(self) -> None:
        '''
            Configures dark scale slider and scrollbar widget styles.

            :exceptions: None.
        '''
        for scale_style in ('TScale', 'Horizontal.TScale'):
            self._style.configure(
                scale_style,
                background=UIColors.BG_SURFACE,
                troughcolor=UIColors.BG_DARK,
                bordercolor=UIColors.BORDER,
                lightcolor=UIColors.BG_SURFACE,
                darkcolor=UIColors.BG_DARK,
            )
        for scroll_style in ('TScrollbar', 'Vertical.TScrollbar'):
            self._style.configure(
                scroll_style,
                background=UIColors.BG_SURFACE,
                troughcolor=UIColors.BG_DARK,
                bordercolor=UIColors.BG_DARK,
                arrowcolor=UIColors.TEXT_MUTED,
                lightcolor=UIColors.BG_SURFACE,
                darkcolor=UIColors.BG_DARK,
            )
            self._style.map(
                scroll_style,
                background=[('active', UIColors.BORDER)],
            )
