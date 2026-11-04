# -*- coding: UTF-8 -*-

'''
Module
    motion_command_test.py
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
    Unit tests for MotionCommand IntEnum.
'''

from __future__ import annotations

from unittest import TestCase, main

from botracked.core.model.motion_command import MotionCommand

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandTest(TestCase):
    '''
        Tests MotionCommand integer enumeration values and membership.
    '''

    def test_members_and_values(self) -> None:
        '''
            Verifies kinematic command member values.

            :exceptions: None.
        '''
        self.assertEqual(int(MotionCommand.STOP), 0)
        self.assertEqual(int(MotionCommand.FORWARD), 1)
        self.assertEqual(int(MotionCommand.BACKWARD), 2)
        self.assertEqual(int(MotionCommand.TURN_LEFT), 3)
        self.assertEqual(int(MotionCommand.TURN_RIGHT), 4)
        self.assertEqual(int(MotionCommand.SPIN_LEFT), 5)
        self.assertEqual(int(MotionCommand.SPIN_RIGHT), 6)

    def test_enumeration_membership(self) -> None:
        '''
            Verifies total count and containment of motion commands.

            :exceptions: None.
        '''
        members = list(MotionCommand)
        self.assertEqual(len(members), 7)
        self.assertIn(MotionCommand.STOP, members)
        self.assertIn(MotionCommand.FORWARD, members)


if __name__ == '__main__':
    main()
