# -*- coding: UTF-8 -*-

'''
Module
    loop.py
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
    Defines WorkerLoop driving iterative connection tasks until stopped.
'''

from __future__ import annotations

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerLoop:
    '''
        Defines class WorkerLoop implementing IWorkerLoop and IRunnableWorker.
        Iterates task execution steps until stop flag is set or step terminates.

        It defines:

            :attributes:
                | _task - Work unit executed during each loop iteration.
                | _stop_flag - Signal flag notifying loop termination.
            :methods:
                | __init__ - Initializes worker loop with task and stop flag.
                | run - Executes iterative task steps until stopped or finished.
                | is_stopped - Checks if loop stop signal flag is active.
    '''

    _task: IWorkerTask
    _stop_flag: ISignalFlag

    def __init__(
        self,
        *,
        task: IWorkerTask,
        stop_flag: ISignalFlag,
    ) -> None:
        '''
            Initializes worker loop with injected task and stop signal flag.

            :param task: Work unit executed during each iteration.
            :param stop_flag: Signal flag notifying loop termination.
            :exceptions: None.
        '''
        self._task = task
        self._stop_flag = stop_flag

    def run(self) -> None:
        '''
            Executes iterative task steps until stopped or finished.

            :exceptions: None.
        '''
        try:
            while not self._stop_flag.is_set():
                should_continue: bool = self._task.execute_step()
                if not should_continue:
                    break
        finally:
            self._task.cleanup()

    def is_stopped(self) -> bool:
        '''
            Checks if loop stop signal flag is active.

            :return: True if stop flag is set, False otherwise.
            :exceptions: None.
        '''
        return self._stop_flag.is_set()
