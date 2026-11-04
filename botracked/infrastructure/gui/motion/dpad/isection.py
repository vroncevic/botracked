# -*- coding: UTF-8 -*-

'''
Module
    isection.py
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
    Defines IMotionDpadSection protocol for D-pad steering leaf section.
'''

from __future__ import annotations

from tkinter.ttk import Frame
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
class IMotionDpadSection(Protocol):
    '''
        Defines structural contract IMotionDpadSection for manual D-pad controls.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | trigger_motion - Dispatches directional command to delegate.
                | trigger_stop - Dispatches immediate stop to delegate.
                | set_enabled - Enables or disables steering buttons.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def trigger_motion(self, cmd: MotionCommand) -> None:
        '''
            Dispatches directional command to delegate.

            :param cmd: MotionCommand enumeration value.
        '''

    def trigger_stop(self) -> None:
        '''
            Dispatches immediate stop to delegate.
        '''

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables steering buttons.

            :param enabled: True if interactive, False otherwise.
        '''
