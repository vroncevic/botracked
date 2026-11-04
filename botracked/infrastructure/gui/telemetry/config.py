# -*- coding: UTF-8 -*-

'''
Module
    config.py
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
    Provides TelemetryPanelConfig frozen dataclass for telemetry labels.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@dataclass(frozen=True, slots=True)
class TelemetryPanelConfig:
    '''
        Immutable UI parameters, card labels, and default offline states.

        It defines:

            :attributes:
                | padding_main - Main container padding in pixels.
                | padding_card - Internal card frame padding in pixels.
                | title_header - Panel header title text.
                | card_mode - Label text for system mode card.
                | card_motion - Label text for motion state card.
                | card_left_motor - Label text for left motor card.
                | card_right_motor - Label text for right motor card.
                | card_speed - Label text for speed card.
                | card_error - Label text for error diagnostics card.
                | card_uptime - Label text for uptime card.
                | default_mode - Initial system mode text.
                | default_motion - Initial motion state text.
                | default_speed - Initial speed display text.
                | default_err - Initial error code display text.
                | default_uptime - Initial uptime display text.
    '''

    padding_main: int = 10
    padding_card: int = 6
    title_header: str = 'LIVE TELEMETRY COCKPIT'
    card_mode: str = 'SYSTEM MODE'
    card_motion: str = 'MOTION STATE'
    card_left_motor: str = 'LEFT TRACK MOTOR'
    card_right_motor: str = 'RIGHT TRACK MOTOR'
    card_speed: str = 'PWM SPEED'
    card_error: str = 'DIAG ERROR CODE'
    card_uptime: str = 'FIRMWARE UPTIME'
    default_mode: str = 'OFFLINE'
    default_motion: str = 'STOP'
    default_speed: str = '0'
    default_err: str = '0x00'
    default_uptime: str = '0.0s'
