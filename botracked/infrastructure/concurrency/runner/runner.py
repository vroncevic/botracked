# -*- coding: UTF-8 -*-

'''
Module
    runner.py
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
    Provides ThreadRunner adapter implementing IThreadRunner contract structurally.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str

from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.infrastructure.concurrency.runner.cycle.icycle import IRunnerCycle
from botracked.infrastructure.concurrency.runner.iexecutor import ITaskExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThreadRunner:
    '''
        Defines class ThreadRunner implementing IThreadRunner contract structurally.
        Manages repeatable worker execution cycles via executor and cycle state.

        It defines:

            :attributes:
                | _executor - Single-thread executor port scheduling worker loops.
                | _cycle - Runner cycle delegate managing flags and completion.
                | _join_timeout - Maximum timeout in seconds when awaiting cycle stop.
            :methods:
                | __init__ - Initializes ThreadRunner with executor, cycle, and timeout.
                | activate - Marks cycle active and schedules worker execution.
                | deactivate - Clears active state and waits for cycle completion.
                | is_active - Checks whether worker execution cycle is active.
                | __str__ - Returns string representation of runner adapter.
    '''

    _executor: ITaskExecutor
    _cycle: IRunnerCycle
    _join_timeout: float

    def __init__(
        self,
        *,
        executor: ITaskExecutor,
        cycle: IRunnerCycle,
        join_timeout: float,
    ) -> None:
        '''
            Initializes ThreadRunner with executor, cycle delegate, and join timeout.

            :param executor: Single-worker task executor port.
            :param cycle: Cycle delegate managing flags and exit cleanup.
            :param join_timeout: Maximum wait duration in seconds on deactivate.
            :exceptions: None.
        '''
        self._executor = executor
        self._cycle = cycle
        self._join_timeout = join_timeout

    def activate(self, worker: IRunnableWorker) -> None:
        '''
            Marks cycle active and schedules worker execution.

            :param worker: Runnable worker instance whose run loop will be executed.
            :exceptions: None.
        '''
        if self._cycle.prepare():
            self._executor.submit(self._cycle, worker)

    def deactivate(self) -> None:
        '''
            Clears active state and waits for cycle completion.

            :exceptions: None.
        '''
        self._cycle.stop(self._join_timeout)

    def is_active(self) -> bool:
        '''
            Checks whether worker execution cycle is active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._cycle.is_active()

    def __str__(self) -> str:
        '''
            Returns string representation of runner adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
