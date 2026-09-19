# -*- coding: UTF-8 -*-

'''
Module
    motion_command.py
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
    Defines MotionCommand enumeration for tracked robot kinematic states.
'''

from __future__ import annotations

from enum import IntEnum

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommand(IntEnum):
    '''
        Discrete kinematic motion commands for dual-track differential chassis.

        It defines:

            :attributes:
                | STOP - Halt motion and lock tracks.
                | FORWARD - Move straight forward.
                | BACKWARD - Move straight backward.
                | TURN_LEFT - Differential turn to the left.
                | TURN_RIGHT - Differential turn to the right.
                | SPIN_LEFT - Counter-rotate tracks left in place.
                | SPIN_RIGHT - Counter-rotate tracks right in place.
            :methods:
                | label - Returns human-readable label for GUI display.
                | from_string - Parses command string into MotionCommand enum.
    '''

    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    TURN_LEFT = 3
    TURN_RIGHT = 4
    SPIN_LEFT = 5
    SPIN_RIGHT = 6

    @property
    def label(self) -> str:
        '''
            Returns human-readable label for GUI display.

            :return: String representation of command.
            :exceptions: None.
        '''
        labels: dict[int, str] = {
            0: 'STOP',
            1: 'FORWARD',
            2: 'BACKWARD',
            3: 'TURN LEFT',
            4: 'TURN RIGHT',
            5: 'SPIN LEFT',
            6: 'SPIN RIGHT',
        }

        return labels.get(self.value, 'UNKNOWN')

    @classmethod
    def from_string(cls, name: str) -> MotionCommand:
        '''
            Parses command string into MotionCommand enum.

            :param name: Command name string.
            :return: Corresponding MotionCommand member.
            :exceptions:
                | ValueError: If string does not match any command.
        '''
        normalized: str = name.strip().upper()

        for member in cls:
            if normalized in (member.name, member.label):
                return member

        raise ValueError(f'Unknown motion command: {name}')
