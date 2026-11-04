# -*- coding: UTF-8 -*-

'''
Module
    trigger_test.py
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
    Unit tests for MotionTrigger action object.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.dpad.trigger.trigger import MotionTrigger
from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionTriggerTest(TestCase):
    '''
        Tests MotionTrigger invocation and bound command lookup.
    '''

    def test_invoke_and_get_command(self) -> None:
        '''
            Verifies invoke dispatches bound MotionCommand to delegate.

            :exceptions: None.
        '''
        delegate = MagicMock(spec=IMotionActionDelegate)
        trig = MotionTrigger(delegate=delegate, command=MotionCommand.SPIN_LEFT)
        self.assertEqual(trig.get_command(), MotionCommand.SPIN_LEFT)
        trig.invoke()
        delegate.handle_motion.assert_called_once_with(MotionCommand.SPIN_LEFT)


if __name__ == '__main__':
    main()
