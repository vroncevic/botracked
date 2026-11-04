# -*- coding: UTF-8 -*-

'''
Module
    task.py
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
    Defines WorkerTask decorator containing connection errors and cleanup.
'''

from __future__ import annotations

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerTask:
    '''
        Defines class WorkerTask implementing IWorkerTask structurally.
        Contains BotConnectionError during iterations and ensures idempotent cleanup.

        It defines:

            :attributes:
                | _task - Wrapped iterative worker task collaborator.
                | _active - Tracks whether cleanup is armed for current run cycle.
            :methods:
                | __init__ - Initializes guarded worker task decorator.
                | execute_step - Executes wrapped step catching BotConnectionError.
                | cleanup - Flushes wrapped task state at most once per cycle.
    '''

    _task: IWorkerTask
    _active: bool

    def __init__(self, task: IWorkerTask) -> None:
        '''
            Initializes guarded worker task decorator with target task.

            :param task: Iterative worker task collaborator.
            :exceptions: None.
        '''
        self._task = task
        self._active = True

    def execute_step(self) -> bool:
        '''
            Executes wrapped task step catching BotConnectionError gracefully.

            :return: True if loop should continue, False on halt or link error.
            :exceptions: None.
        '''
        self._active = True
        try:
            return self._task.execute_step()
        except BotConnectionError:
            return False

    def cleanup(self) -> None:
        '''
            Flushes wrapped task state idempotently across loop and stop paths.

            :exceptions: None.
        '''
        if self._active:
            self._active = False
            self._task.cleanup()
