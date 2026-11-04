# -*- coding: UTF-8 -*-

'''
Module
    idelegate.py
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
    Defines IMotionActionDelegate protocol for manual motion UI actions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.model.motion_command import MotionCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IMotionActionDelegate(Protocol):
    '''
        Defines structural contract IMotionActionDelegate for steering actions.

        It defines:

            :methods:
                | handle_motion - Dispatches directional motion command.
                | handle_speed - Updates active PWM duty speed level.
                | handle_stop - Dispatches immediate emergency motor stop.
                | handle_ping - Sends firmware link health ping.
                | handle_clear_errors - Sends firmware fault clear command.
    '''

    def handle_motion(self, cmd: MotionCommand) -> None:
        '''
            Dispatches directional motion command.

            :param cmd: MotionCommand direction enumeration value.
        '''

    def handle_speed(self, speed: int) -> None:
        '''
            Updates active locomotion PWM speed level.

            :param speed: PWM duty speed integer in range [0, 255].
        '''

    def handle_stop(self) -> None:
        '''
            Dispatches immediate emergency motor stop.
        '''

    def handle_ping(self) -> None:
        '''
            Sends firmware link health verification ping.
        '''

    def handle_clear_errors(self) -> None:
        '''
            Sends firmware fault clear command.
        '''
