# -*- coding: UTF-8 -*-

'''
Module
    jog_panel_callbacks.py
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
    Parameter bundle encapsulating callbacks for manual jog controls.
'''

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from botracked.core.model.motion_command import MotionCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class JogPanelCallbacks:
    '''
        Defines class JogPanelCallbacks with attribute(s) and method(s).
        Parameter bundle encapsulating event callbacks for manual robot jog controls.

        It defines:

            :attributes:
                | on_motion - Callback for dispatching motion commands.
                | on_speed - Callback for adjusting speed PWM.
                | on_stop - Callback for issuing emergency or normal stop.
                | on_ping - Callback for sending ping diagnostic request.
                | on_clear_err - Callback for clearing firmware errors.
            :methods: None.
    '''

    on_motion: Callable[[MotionCommand], bool]
    on_speed: Callable[[int], bool]
    on_stop: Callable[[], bool]
    on_ping: Callable[[], bool]
    on_clear_err: Callable[[], bool]
