# -*- coding: UTF-8 -*-

'''
Module
    style.py
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
    Provides StyleConfigurator applying custom ttk themes and widget styles.
'''

from __future__ import annotations

from tkinter.ttk import Style

from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StyleConfigurator:
    '''
        Defines class StyleConfigurator with attribute(s) and method(s).
        Configures ttk style manager with custom dark robotics palette.

        It defines:

            :attributes: None.
            :methods:
                | get_theme_palette - Returns dictionary of theme color tokens.
                | apply - Applies theme rules to standard ttk widgets.
                | _configure_frames - Configures frame widget styles.
                | _configure_labels - Configures label widget styles.
                | _configure_buttons - Configures button widget styles.
    '''

    @classmethod
    def get_theme_palette(cls) -> dict[str, str]:
        '''
            Returns dictionary mapping of UI theme color tokens.

            :return: Mapping of color tokens to hex values.
            :exceptions: None.
        '''
        return {
            'bg_dark': UIColors.BG_DARK,
            'bg_panel': UIColors.BG_PANEL,
            'bg_header': UIColors.BG_HEADER,
            'bg_surface': UIColors.BG_SURFACE,
            'text_main': UIColors.TEXT_MAIN,
            'text_muted': UIColors.TEXT_MUTED,
            'cyan': UIColors.CYAN,
            'green': UIColors.GREEN,
            'red': UIColors.RED,
            'blue': UIColors.BLUE,
        }

    @classmethod
    def apply(cls, style: Style) -> None:
        '''
            Applies theme rules to standard ttk widgets.

            :param style: Tkinter ttk Style instance.
            :exceptions: None.
        '''
        style.theme_use('clam')
        cls._configure_frames(style)
        cls._configure_labels(style)
        cls._configure_buttons(style)

    @classmethod
    def _configure_frames(cls, style: Style) -> None:
        '''
            Configures frame widget styles.

            :param style: Tkinter ttk Style instance.
            :exceptions: None.
        '''
        style.configure('TFrame', background=UIColors.BG_DARK)
        style.configure('Panel.TFrame', background=UIColors.BG_PANEL, relief='flat')
        style.configure('Surface.TFrame', background=UIColors.BG_SURFACE, relief='flat')

    @classmethod
    def _configure_labels(cls, style: Style) -> None:
        '''
            Configures label widget styles.

            :param style: Tkinter ttk Style instance.
            :exceptions: None.
        '''
        style.configure('TLabel', background=UIColors.BG_DARK, foreground=UIColors.TEXT_MAIN, font=('Helvetica', 10))
        style.configure('Panel.TLabel', background=UIColors.BG_PANEL, foreground=UIColors.TEXT_MAIN, font=('Helvetica', 10))
        style.configure(
            'Header.TLabel', background=UIColors.BG_HEADER,
            foreground=UIColors.CYAN, font=('Helvetica', 11, 'bold')
        )
        style.configure(
            'CardTitle.TLabel', background=UIColors.BG_SURFACE,
            foreground=UIColors.TEXT_MUTED, font=('Helvetica', 9)
        )
        style.configure(
            'CardValue.TLabel', background=UIColors.BG_SURFACE,
            foreground=UIColors.GREEN, font=('Helvetica', 13, 'bold')
        )

    @classmethod
    def _configure_buttons(cls, style: Style) -> None:
        '''
            Configures button widget styles.

            :param style: Tkinter ttk Style instance.
            :exceptions: None.
        '''
        style.configure(
            'TButton', background=UIColors.BG_SURFACE,
            foreground=UIColors.TEXT_MAIN, borderwidth=1,
            focuscolor='none', font=('Helvetica', 9, 'bold')
        )
        style.map('TButton', background=[('active', UIColors.BORDER), ('pressed', UIColors.BG_HEADER)])

        style.configure(
            'Accent.TButton', background=UIColors.BLUE,
            foreground=UIColors.BG_HEADER, font=('Helvetica', 9, 'bold')
        )
        style.map('Accent.TButton', background=[('active', UIColors.CYAN), ('pressed', UIColors.BLUE)])

        style.configure(
            'Danger.TButton', background=UIColors.RED,
            foreground=UIColors.BG_HEADER, font=('Helvetica', 10, 'bold')
        )
        style.map('Danger.TButton', background=[('active', '#F39CA8'), ('pressed', '#E06C75')])

        style.configure(
            'Success.TButton', background=UIColors.GREEN,
            foreground=UIColors.BG_HEADER, font=('Helvetica', 9, 'bold')
        )
        style.map('Success.TButton', background=[('active', '#B5E8B0'), ('pressed', '#98C379')])
