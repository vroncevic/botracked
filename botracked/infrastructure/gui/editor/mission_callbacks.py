# -*- coding: UTF-8 -*-

'''
Module
    mission_callbacks.py
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
    Parameter bundle encapsulating callbacks for mission execution management.
'''

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from botracked.core.model.dsl.compiled_step import CompiledStep

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class MissionCallbacks:
    '''
        Defines class MissionCallbacks with attribute(s) and method(s).
        Parameter bundle encapsulating event callbacks for mission routine execution.

        It defines:

            :attributes:
                | on_start - Callback to start compiled mission execution.
                | on_pause - Callback to pause active mission.
                | on_resume - Callback to resume paused mission.
                | on_abort - Callback to abort mission immediately.
            :methods: None.
    '''

    on_start: Callable[[list[CompiledStep]], None]
    on_pause: Callable[[], None]
    on_resume: Callable[[], None]
    on_abort: Callable[[], None]
