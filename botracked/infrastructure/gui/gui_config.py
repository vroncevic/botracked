# -*- coding: UTF-8 -*-

'''
Module
    gui_config.py
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
    Provides GuiConfig dataclass encapsulating top-level window settings.
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
class GuiConfig:
    '''
        Defines class GuiConfig with attribute(s) and method(s).
        Immutable configuration parameters for primary GUI window.

        It defines:

            :attributes:
                | window_title - Main window title string.
                | min_width - Minimum window width in pixels.
                | min_height - Minimum window height in pixels.
                | padding_row_x - Horizontal padding for grid rows.
                | padding_cockpit_y_top - Top padding for cockpit row.
                | padding_cockpit_y_bot - Bottom padding for cockpit row.
                | padding_editor_y_top - Top padding for editor row.
                | padding_editor_y_bot - Bottom padding for editor row.
                | padding_log_y_bot - Bottom padding for log row.
            :methods: None.
    '''

    window_title: str = (
        'botracked — Dual-Track Differential Robot Cockpit & Mission Studio'
    )
    min_width: int = 1200
    min_height: int = 800
    padding_row_x: int = 8
    padding_cockpit_y_top: int = 4
    padding_cockpit_y_bot: int = 2
    padding_editor_y_top: int = 2
    padding_editor_y_bot: int = 4
    padding_log_y_bot: int = 8
