# -*- coding: UTF-8 -*-

'''
Module
    runner_test.py
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
    Unit tests for MissionRunner.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.motion.runner.runner import MissionRunner
from botracked.core.service.motion.runner.worker.iworker import IMissionExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionRunnerTestCase(TestCase):
    '''
        Verifies MissionRunner start, pause, resume, abort, and running state.
    '''

    def test_lifecycle_commands(self) -> None:
        '''
            Verifies empty rejection, start activation, pause, resume, abort.

            :exceptions: None.
        '''
        worker = Mock(spec=IMissionExecutionWorker)
        controller = Mock(spec=ILoopController)
        controller.is_running.side_effect = [False, True, False]
        pause_flag = Event()
        mission = MissionRunner(
            worker=worker,
            controller=controller,
            pause_flag=pause_flag,
        )
        step = CompiledStep(
            frames=(b'\x01',),
            duration_sec=0.1,
            auto_stop_after=False,
            description='PING',
            line_number=1,
        )

        self.assertFalse(mission.start(()))
        self.assertFalse(mission.is_running())

        self.assertTrue(mission.start((step,)))
        worker.load_steps.assert_called_once_with((step,))
        controller.start.assert_called_once_with(worker)
        self.assertTrue(mission.is_running())

        mission.pause()
        self.assertTrue(pause_flag.is_set())
        mission.resume()
        self.assertFalse(pause_flag.is_set())

        mission.abort()
        self.assertEqual(controller.stop.call_count, 2)
        self.assertFalse(mission.is_running())


if __name__ == '__main__':
    main()
