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
    Unit tests for ThreadRunner adapter lifecycle management.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.infrastructure.concurrency.runner.cycle.icycle import IRunnerCycle
from botracked.infrastructure.concurrency.runner.iexecutor import ITaskExecutor
from botracked.infrastructure.concurrency.runner.runner import ThreadRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThreadRunnerTest(TestCase):
    '''
        Verifies ThreadRunner activate, deactivate, active state, and str.
    '''

    def test_lifecycle_transitions_and_string(self) -> None:
        '''
            Verifies ThreadRunner delegates cycle preparation, submission, and stop.

            :exceptions: None.
        '''
        executor = Mock(spec=ITaskExecutor)
        cycle = Mock(spec=IRunnerCycle)
        cycle.prepare.side_effect = [True, False]
        cycle.is_active.side_effect = [False, True, False]
        worker = Mock(spec=IRunnableWorker)
        runner = ThreadRunner(
            executor=executor,
            cycle=cycle,
            join_timeout=0.02,
        )

        self.assertFalse(runner.is_active())
        runner.activate(worker)
        self.assertTrue(runner.is_active())
        executor.submit.assert_called_once_with(cycle, worker)

        runner.activate(worker)
        self.assertEqual(executor.submit.call_count, 1)

        runner.deactivate()
        cycle.stop.assert_called_once_with(0.02)
        self.assertFalse(runner.is_active())
        self.assertIn('ThreadRunner', str(runner))


if __name__ == '__main__':
    main()
