# -*- coding: UTF-8 -*-

'''
Module
    colors.py
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
    Defines UI color constants for dark theme cockpit styling.
'''

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class UIColors:
    '''
        Defines class UIColors with attribute(s) and method(s).
        Palette constants for high-contrast dark robotics cockpit interface.

        It defines:

            :attributes:
                | BG_DARK - Main background color.
                | BG_PANEL - Secondary panel background color.
                | BG_HEADER - Header bar background color.
                | BG_SURFACE - Surface widget background color.
                | TEXT_MAIN - Primary text color.
                | TEXT_MUTED - Secondary muted text color.
                | TEXT_DIM - Dim helper text color.
                | BORDER - Border divider color.
                | GREEN - Success/online state color.
                | RED - Error/offline state color.
                | AMBER - Warning/standby state color.
                | BLUE - Accent/information color.
                | CYAN - Alternative accent color.
                | PURPLE - Special highlights color.
            :methods: None.
    '''

    BG_DARK: ClassVar[str] = '#1E1E2E'
    BG_PANEL: ClassVar[str] = '#25263A'
    BG_HEADER: ClassVar[str] = '#181825'
    BG_SURFACE: ClassVar[str] = '#313244'
    TEXT_MAIN: ClassVar[str] = '#CDD6F4'
    TEXT_MUTED: ClassVar[str] = '#A6ADC8'
    TEXT_DIM: ClassVar[str] = '#6C7086'
    BORDER: ClassVar[str] = '#45475A'

    # Telemetry and state indicators
    GREEN: ClassVar[str] = '#A6E3A1'
    RED: ClassVar[str] = '#F38BA8'
    AMBER: ClassVar[str] = '#F9E2AF'
    BLUE: ClassVar[str] = '#89B4FA'
    CYAN: ClassVar[str] = '#89DCEB'
    PURPLE: ClassVar[str] = '#CBA6F7'
