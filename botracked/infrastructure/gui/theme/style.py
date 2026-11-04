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
    Provides StyleConfigurator applying custom dark robotics ttk styles.
'''

from __future__ import annotations

from tkinter.ttk import Style
from typing import ClassVar

from botracked.infrastructure.gui.theme.colors import UIColors
from botracked.infrastructure.gui.theme.controls.icontrols import IControlStyleConfigurator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class StyleConfigurator:
    '''
        Defines class StyleConfigurator implementing IStyleConfigurator.
        Configures ttk Style manager with high-contrast dark robotics palette.

        It defines:

            :attributes:
                | THEME_NAME - Base ttk theme engine identifier.
                | FONT_FAMILY - Primary UI sans-serif font family.
                | FONT_BASE - Standard body label font tuple.
                | FONT_HEADER - Panel header title font tuple.
                | FONT_CARD_TITLE - Metric card title font tuple.
                | FONT_CARD_VALUE - Metric card value font tuple.
                | FONT_BUTTON - Standard action button font tuple.
                | FONT_DANGER - Danger button bold font tuple.
                | BTN_PADDING - Standard horizontal and vertical button pad.
                | _style - Bound ttk Style manager instance.
                | _controls - Interactive control style configurator port.
            :methods:
                | __init__ - Initializes configurator with style and controls.
                | get_theme_palette - Returns dictionary of theme color tokens.
                | apply - Applies theme rules to standard ttk widgets.
                | configure_frames - Configures frame widget styles.
                | configure_labels - Configures label widget styles.
                | configure_buttons - Configures button widget styles.
    '''

    THEME_NAME: ClassVar[str] = 'clam'
    FONT_FAMILY: ClassVar[str] = 'DejaVu Sans'
    FONT_BASE: ClassVar[tuple[str, int]] = ('DejaVu Sans', 10)
    FONT_HEADER: ClassVar[tuple[str, int, str]] = ('DejaVu Sans', 11, 'bold')
    FONT_CARD_TITLE: ClassVar[tuple[str, int]] = ('DejaVu Sans', 9)
    FONT_CARD_VALUE: ClassVar[tuple[str, int, str]] = (
        'DejaVu Sans',
        13,
        'bold',
    )
    FONT_BUTTON: ClassVar[tuple[str, int, str]] = ('DejaVu Sans', 9, 'bold')
    FONT_DANGER: ClassVar[tuple[str, int, str]] = ('DejaVu Sans', 10, 'bold')
    BTN_PADDING: ClassVar[tuple[int, int]] = (4, 4)

    _style: Style
    _controls: IControlStyleConfigurator

    def __init__(
        self,
        style: Style,
        controls: IControlStyleConfigurator,
    ) -> None:
        '''
            Initializes configurator with ttk Style and control configurator.

            :param style: Tkinter ttk Style instance.
            :param controls: Interactive control style configurator port.
            :exceptions: None.
        '''
        self._style = style
        self._controls = controls

    def get_theme_palette(self) -> dict[str, str]:
        '''
            Returns dictionary mapping of UI theme color tokens.

            :return: Mapping of color tokens to hex values.
            :exceptions: None.
        '''
        return {
            'bg_dark': str(UIColors.BG_DARK),
            'bg_panel': str(UIColors.BG_PANEL),
            'bg_header': str(UIColors.BG_HEADER),
            'bg_surface': str(UIColors.BG_SURFACE),
            'text_main': str(UIColors.TEXT_MAIN),
            'text_muted': str(UIColors.TEXT_MUTED),
            'cyan': str(UIColors.CYAN),
            'green': str(UIColors.GREEN),
            'red': str(UIColors.RED),
            'blue': str(UIColors.BLUE),
        }

    def apply(self) -> None:
        '''
            Applies theme rules to standard ttk widgets.

            :exceptions: None.
        '''
        self._style.theme_use(self.THEME_NAME)
        self._style.configure(
            '.',
            background=UIColors.BG_DARK,
            foreground=UIColors.TEXT_MAIN,
        )
        self.configure_frames()
        self.configure_labels()
        self.configure_buttons()
        self._controls.apply()

    def configure_frames(self) -> None:
        '''
            Configures frame widget styles.

            :exceptions: None.
        '''
        self._style.configure('TFrame', background=UIColors.BG_DARK)
        self._style.configure(
            'Panel.TFrame', background=UIColors.BG_PANEL, relief='flat'
        )
        self._style.configure(
            'Surface.TFrame', background=UIColors.BG_SURFACE, relief='flat'
        )

    def configure_labels(self) -> None:
        '''
            Configures label widget styles.

            :exceptions: None.
        '''
        label_specs: tuple[tuple[str, str, str, tuple[object, ...]], ...] = (
            ('TLabel', UIColors.BG_DARK, UIColors.TEXT_MAIN, self.FONT_BASE),
            ('Panel.TLabel', UIColors.BG_PANEL, UIColors.TEXT_MAIN, self.FONT_BASE),
            ('Surface.TLabel', UIColors.BG_SURFACE, UIColors.TEXT_MAIN, self.FONT_BASE),
            ('Header.TLabel', UIColors.BG_HEADER, UIColors.CYAN, self.FONT_HEADER),
            ('PanelHeader.TLabel', UIColors.BG_PANEL, UIColors.CYAN, self.FONT_HEADER),
            ('SurfaceHeader.TLabel', UIColors.BG_SURFACE, UIColors.CYAN, self.FONT_HEADER),
            ('CardTitle.TLabel', UIColors.BG_SURFACE, UIColors.TEXT_MUTED, self.FONT_CARD_TITLE),
            ('CardValue.TLabel', UIColors.BG_SURFACE, UIColors.GREEN, self.FONT_CARD_VALUE),
        )
        for style_name, bg_col, fg_col, font_spec in label_specs:
            self._style.configure(
                style_name,
                background=bg_col,
                foreground=fg_col,
                font=font_spec,
            )
            self._style.map(
                style_name,
                background=[('active', bg_col), ('!active', bg_col)],
            )

    def configure_buttons(self) -> None:
        '''
            Configures button widget styles.

            :exceptions: None.
        '''
        self._style.configure(
            'TButton',
            background=UIColors.BG_SURFACE,
            foreground=UIColors.TEXT_MAIN,
            borderwidth=1,
            padding=self.BTN_PADDING,
            focuscolor='none',
            font=self.FONT_BUTTON,
        )
        self._style.map(
            'TButton',
            background=[
                ('disabled', UIColors.BG_PANEL),
                ('pressed', UIColors.BG_HEADER),
                ('active', UIColors.BORDER),
            ],
            foreground=[
                ('disabled', UIColors.TEXT_DIM),
                ('!disabled', UIColors.TEXT_MAIN),
            ],
        )
        self._style.configure(
            'Accent.TButton',
            background=UIColors.BLUE,
            foreground=UIColors.BG_HEADER,
            padding=self.BTN_PADDING,
            font=self.FONT_BUTTON,
        )
        self._style.map(
            'Accent.TButton',
            background=[('active', UIColors.CYAN), ('pressed', UIColors.BLUE)],
            foreground=[('!disabled', UIColors.BG_HEADER)],
        )
        self._style.configure(
            'Danger.TButton',
            background=UIColors.RED,
            foreground=UIColors.BG_HEADER,
            padding=self.BTN_PADDING,
            font=self.FONT_DANGER,
        )
        self._style.map(
            'Danger.TButton',
            background=[
                ('active', UIColors.RED_ACTIVE),
                ('pressed', UIColors.RED_PRESSED),
            ],
            foreground=[('!disabled', UIColors.BG_HEADER)],
        )
        self._style.configure(
            'Success.TButton',
            background=UIColors.GREEN,
            foreground=UIColors.BG_HEADER,
            padding=self.BTN_PADDING,
            font=self.FONT_BUTTON,
        )
        self._style.map(
            'Success.TButton',
            background=[
                ('active', UIColors.GREEN_ACTIVE),
                ('pressed', UIColors.GREEN_PRESSED),
            ],
            foreground=[('!disabled', UIColors.BG_HEADER)],
        )
