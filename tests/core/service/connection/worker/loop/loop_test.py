# -*- coding: UTF-8 -*-

'''
Module
    loop_test.py
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
    Unit tests for WorkerLoop iterative task execution and cleanup.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.connection.worker.loop.loop import WorkerLoop
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerLoopTest(TestCase):
    '''
        Verifies WorkerLoop iterative step execution, stop check, and cleanup.
    '''

    def test_run_iterates_until_step_returns_false_and_cleans_up(self) -> None:
        '''
            Verifies run loop iterates execute_step until False and runs cleanup.

            :exceptions: None.
        '''
        stop_flag = Event()
        task = Mock(spec=IWorkerTask)
        task.execute_step.side_effect = [True, False]
        loop = WorkerLoop(task=task, stop_flag=stop_flag)

        self.assertFalse(loop.is_stopped())
        loop.run()

        self.assertEqual(task.execute_step.call_count, 2)
        task.cleanup.assert_called_once()

    def test_run_exits_immediately_when_stop_flag_set(self) -> None:
        '''
            Verifies run loop skips step execution when stop_flag is set.

            :exceptions: None.
        '''
        stop_flag = Event()
        stop_flag.set()
        task = Mock(spec=IWorkerTask)
        loop = WorkerLoop(task=task, stop_flag=stop_flag)

        self.assertTrue(loop.is_stopped())
        loop.run()

        task.execute_step.assert_not_called()
        task.cleanup.assert_called_once()


if __name__ == '__main__':
    main()
