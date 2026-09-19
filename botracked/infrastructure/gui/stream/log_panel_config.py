# -*- coding: UTF-8 -*-

'''
Module
    log_panel_config.py
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
    Provides LogPanelConfig dataclass encapsulating log panel UI literals.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class LogPanelConfig:
    '''
        Defines class LogPanelConfig with attribute(s) and method(s).
        Immutable UI parameters, button labels, and logging formats for LogPanel.

        It defines:

            :attributes:
                | padding_main - Main container padding in pixels.
                | padding_header - Header container padding in pixels.
                | title_header - Panel header title text.
                | btn_clear - Label text for clear button.
                | btn_copy - Label text for copy button.
                | btn_select_all - Label text for select all button.
                | font_family - Log text font family name.
                | font_size - Log text font size in points.
                | log_height - Log area height in lines.
                | time_format - Timestamp format string.
            :methods: None.
    '''

    padding_main: int = 6
    padding_header: int = 6
    title_header: str = 'BINARY PROTOCOL PACKET STREAM'
    btn_clear: str = 'Clear'
    btn_copy: str = 'Copy'
    btn_select_all: str = 'Select All'
    font_family: str = 'Courier'
    font_size: int = 10
    log_height: int = 8
    time_format: str = '%H:%M:%S.%f'
