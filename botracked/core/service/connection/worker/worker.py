# -*- coding: UTF-8 -*-

'''
Module
    worker.py
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
    Defines ConnectionWorker orchestrating background I/O loop and task cleanup.
'''

from __future__ import annotations

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.connection.worker.loop.iloop import IWorkerLoop
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionWorker:
    '''
        Defines class ConnectionWorker implementing IConnectionWorker structurally.
        Manages start, stop, and cleanup lifecycle of background connection loop.

        It defines:

            :attributes:
                | _loop - Runnable worker loop executing iterative task steps.
                | _task - Work unit cleaned up upon explicit stop.
                | _controller - Concurrency loop controller driving execution.
            :methods:
                | __init__ - Initializes worker with loop, task, and controller.
                | start - Activates background worker execution via controller.
                | stop - Stops loop execution and cleans up task state.
                | is_running - Checks if background worker is currently active.
    '''

    _loop: IWorkerLoop
    _task: IWorkerTask
    _controller: ILoopController

    def __init__(
        self,
        *,
        loop: IWorkerLoop,
        task: IWorkerTask,
        controller: ILoopController,
    ) -> None:
        '''
            Initializes connection worker with loop, task, and loop controller.

            :param loop: Runnable worker loop executing iterative steps.
            :param task: Work unit cleaned up upon stop.
            :param controller: Concurrency loop controller port.
            :exceptions: None.
        '''
        self._loop = loop
        self._task = task
        self._controller = controller

    def start(self) -> None:
        '''
            Activates background worker execution via loop controller port.

            :exceptions: None.
        '''
        self._controller.start(self._loop)

    def stop(self) -> None:
        '''
            Stops worker execution and cleans up task state.

            :exceptions: None.
        '''
        self._controller.stop()
        self._task.cleanup()

    def is_running(self) -> bool:
        '''
            Checks if background worker is currently active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._controller.is_running()
