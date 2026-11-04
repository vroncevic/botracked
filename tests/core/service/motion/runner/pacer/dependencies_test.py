# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for MissionPacerDependencies immutable bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.motion.runner.pacer.dependencies import MissionPacerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionPacerDependenciesTest(TestCase):
    '''
        Verifies MissionPacerDependencies fields and immutability.
    '''

    def test_fields_and_frozen(self) -> None:
        '''
            Verifies pause_flag, stop_flag, tick_interval_sec, and frozen check.

            :exceptions: None.
        '''
        pause = Mock(spec=ISignalFlag)
        stop = Mock(spec=ISignalFlag)
        clock = Mock(spec=IClock)
        deps = MissionPacerDependencies(
            pause_flag=pause,
            stop_flag=stop,
            clock=clock,
            tick_interval_sec=0.05,
        )
        self.assertIs(deps.pause_flag, pause)
        self.assertIs(deps.stop_flag, stop)
        self.assertIs(deps.clock, clock)
        self.assertEqual(deps.tick_interval_sec, 0.05)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'tick_interval_sec', 0.2)


if __name__ == '__main__':
    main()
