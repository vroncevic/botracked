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
    Defines MissionRunner coordinating asynchronous mission routine execution.
'''

from __future__ import annotations

from collections.abc import Sequence

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.motion.runner.worker.iworker import IMissionExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionRunner:
    '''
        Defines class MissionRunner implementing IMissionRunner structurally.
        Coordinates lifecycle of background mission worker execution cycles.

        It defines:

            :attributes:
                | _worker - Execution worker port processing compiled steps.
                | _controller - Concurrency loop controller managing cycle state.
                | _pause_flag - Signal flag indicating paused progression.
            :methods:
                | __init__ - Initializes runner with worker, controller, and pause flag.
                | start - Starts mission execution on background controller.
                | pause - Pauses active mission progression.
                | resume - Resumes paused mission progression.
                | abort - Cancels active mission and waits for worker stop.
                | is_running - Checks if mission execution cycle is active.
    '''

    _worker: IMissionExecutionWorker
    _controller: ILoopController
    _pause_flag: ISignalFlag

    def __init__(
        self,
        *,
        worker: IMissionExecutionWorker,
        controller: ILoopController,
        pause_flag: ISignalFlag,
    ) -> None:
        '''
            Initializes runner with worker, loop controller, and pause flag.

            :param worker: Execution worker port processing compiled steps.
            :param controller: Concurrency loop controller managing cycle state.
            :param pause_flag: Signal flag indicating paused progression.
            :exceptions: None.
        '''
        self._worker = worker
        self._controller = controller
        self._pause_flag = pause_flag

    def start(self, steps: Sequence[CompiledStep]) -> bool:
        '''
            Starts mission execution on background loop controller.

            :param steps: Ordered sequence of compiled mission steps.
            :return: True if mission was started, False if empty.
            :exceptions: None.
        '''
        if not steps:
            return False

        self.abort()
        self._pause_flag.clear()
        self._worker.load_steps(steps)
        self._controller.start(self._worker)
        return True

    def pause(self) -> None:
        '''
            Pauses active mission progression.

            :exceptions: None.
        '''
        self._pause_flag.set()

    def resume(self) -> None:
        '''
            Resumes paused mission progression.

            :exceptions: None.
        '''
        self._pause_flag.clear()

    def abort(self) -> None:
        '''
            Cancels active mission and waits for worker cycle completion.

            :exceptions: None.
        '''
        self._pause_flag.clear()
        self._controller.stop()

    def is_running(self) -> bool:
        '''
            Checks if mission execution cycle is active.

            :return: True if background cycle is active, False otherwise.
            :exceptions: None.
        '''
        return self._controller.is_running()
