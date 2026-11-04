# -*- coding: UTF-8 -*-

'''
Module
    mission_test.py
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
    Unit tests for MissionAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.motion.protocol.iactuator import IMissionActuator
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.setup.service.mission import MissionAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionAssemblerTest(TestCase):
    '''
        Tests MissionAssembler mission execution wiring.
    '''

    def test_assemble_and_version(self) -> None:
        '''
            Verifies MissionAssembler returns configured IMissionRunner.

            :exceptions: None.
        '''
        clock = MagicMock(spec=IClock)
        actuator = MagicMock(spec=IMissionActuator)
        runner: IMissionRunner = MissionAssembler.assemble(
            clock=clock, actuator=actuator
        )
        self.assertIsInstance(runner, IMissionRunner)
        self.assertEqual(MissionAssembler.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
