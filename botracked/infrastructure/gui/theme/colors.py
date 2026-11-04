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
    Defines UIColors string enumeration for dark robotics cockpit styling.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@unique
class UIColors(StrEnum):
    '''
        Defines enumeration UIColors for high-contrast dark cockpit interface.

        It defines:

            :attributes:
                | BG_DARK - Main window background color.
                | BG_PANEL - Secondary panel background color.
                | BG_HEADER - Header bar background color.
                | BG_SURFACE - Surface widget background color.
                | TEXT_MAIN - Primary text foreground color.
                | TEXT_MUTED - Secondary muted text foreground color.
                | TEXT_DIM - Dim helper and timestamp text color.
                | BORDER - Divider and active button border color.
                | GREEN - Online and success indicator color.
                | GREEN_ACTIVE - Active hover color for success buttons.
                | GREEN_PRESSED - Pressed state color for success buttons.
                | RED - Offline and fault indicator color.
                | RED_ACTIVE - Active hover color for danger buttons.
                | RED_PRESSED - Pressed state color for danger buttons.
                | AMBER - Warning and hexadecimal stream color.
                | BLUE - Primary accent color.
                | CYAN - Secondary accent and header highlight color.
                | PURPLE - Special highlight token color.
    '''

    BG_DARK = '#1E1E2E'
    BG_PANEL = '#25263A'
    BG_HEADER = '#181825'
    BG_SURFACE = '#313244'
    TEXT_MAIN = '#CDD6F4'
    TEXT_MUTED = '#A6ADC8'
    TEXT_DIM = '#6C7086'
    BORDER = '#45475A'
    GREEN = '#A6E3A1'
    GREEN_ACTIVE = '#B5E8B0'
    GREEN_PRESSED = '#98C379'
    RED = '#F38BA8'
    RED_ACTIVE = '#F39CA8'
    RED_PRESSED = '#E06C75'
    AMBER = '#F9E2AF'
    BLUE = '#89B4FA'
    CYAN = '#89DCEB'
    PURPLE = '#CBA6F7'
