# -*- coding: UTF-8 -*-

'''
Module
    jog_panel_config.py
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
    Provides JogPanelConfig dataclass encapsulating jog panel UI literals.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class JogPanelConfig:
    '''
        Defines class JogPanelConfig with attribute(s) and method(s).
        Immutable UI parameters and string tokens for JogPanel.

        It defines:

            :attributes:
                | default_speed - Default speed slider value.
                | max_speed - Maximum speed value integer.
                | padding_main - Main container padding in pixels.
                | padding_section - Internal section padding in pixels.
                | header_text - Panel header title text.
                | spin_l_text - Label for spin left button.
                | fwd_text - Label for forward button.
                | spin_r_text - Label for spin right button.
                | left_text - Label for turn left button.
                | stop_text - Label for stop button.
                | right_text - Label for turn right button.
                | bwd_text - Label for backward button.
                | estop_text - Label for emergency stop button.
                | ping_text - Label for ping link button.
                | clear_err_text - Label for clear errors button.
                | btn_width_dpad - Width for d-pad direction buttons.
                | btn_width_center - Width for center action buttons.
            :methods: None.
    '''

    default_speed: float = 180.0
    max_speed: int = 255
    padding_main: int = 10
    padding_section: int = 8
    header_text: str = 'MANUAL JOG & KINEMATICS'
    spin_l_text: str = '↺ SPIN L (Q)'
    fwd_text: str = '▲ FORWARD (W)'
    spin_r_text: str = '↻ SPIN R (E)'
    left_text: str = '◀ LEFT (A)'
    stop_text: str = '■ STOP (Space)'
    right_text: str = '▶ RIGHT (D)'
    bwd_text: str = '▼ BACKWARD (S)'
    estop_text: str = 'EMERGENCY STOP'
    ping_text: str = 'PING LINK'
    clear_err_text: str = 'CLEAR ERRORS'
    btn_width_dpad: int = 12
    btn_width_center: int = 14
