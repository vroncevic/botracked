# -*- coding: UTF-8 -*-

'''
Module
    cycle_test.py
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
    Unit tests for RunnerCycle action adapter flag cleanup and execution.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.infrastructure.concurrency.runner.cycle.cycle import RunnerCycle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RunnerCycleTest(TestCase):
    '''
        Verifies RunnerCycle worker execution, flag cleanup, and string representation.
    '''

    def test_prepare_call_stop_and_flags(self) -> None:
        '''
            Verifies prepare, __call__, stop, is_active, and string representation.

            :exceptions: None.
        '''
        active = Event()
        stopped = Event()
        stopped.set()
        worker = Mock(spec=IRunnableWorker)
        cycle = RunnerCycle(active_flag=active, stopped_flag=stopped)

        self.assertFalse(cycle.is_active())
        self.assertTrue(cycle.prepare())
        self.assertTrue(cycle.is_active())
        self.assertFalse(stopped.is_set())
        self.assertFalse(cycle.prepare())

        cycle(worker)

        worker.run.assert_called_once()
        self.assertFalse(cycle.is_active())
        self.assertTrue(stopped.is_set())

        active.set()
        cycle.stop(0.02)
        self.assertFalse(cycle.is_active())
        cycle.stop(0.02)
        self.assertIn('RunnerCycle', str(cycle))

    def test_call_cleans_flags_on_worker_exception(self) -> None:
        '''
            Verifies cycle clears active and sets stopped even if worker raises.

            :exceptions: None.
        '''
        active = Event()
        active.set()
        stopped = Event()
        worker = Mock(spec=IRunnableWorker)
        worker.run.side_effect = RuntimeError('worker failure')
        cycle = RunnerCycle(active_flag=active, stopped_flag=stopped)

        with self.assertRaises(RuntimeError):
            cycle(worker)

        self.assertFalse(cycle.is_active())
        self.assertTrue(stopped.is_set())


if __name__ == '__main__':
    main()
