# -*- coding: UTF-8 -*-

'''
Module
    icycle.py
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
    Defines structural protocol IRunnerCycle encapsulating worker cycle completion.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from botracked.core.service.concurrency.irunnable import IRunnableWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IRunnerCycle(Protocol):
    '''
        Defines structural contract IRunnerCycle managing cycle flags and execution.

        It defines:

            :methods:
                | prepare - Marks cycle active when currently idle.
                | __call__ - Executes worker loop and signals cycle completion.
                | stop - Clears active state and waits for cycle termination.
                | is_active - Checks whether active cycle signal flag is set.
    '''

    def prepare(self) -> bool:
        '''
            Marks cycle active when currently idle.

            :return: True if cycle transitioned to active, False if already active.
        '''

    def __call__(self, worker: IRunnableWorker) -> None:
        '''
            Executes worker loop and guarantees cycle state cleanup on exit.

            :param worker: Runnable worker instance to execute on worker thread.
        '''

    def stop(self, timeout: float) -> None:
        '''
            Clears active state and waits for cycle termination.

            :param timeout: Maximum wait duration in seconds.
        '''

    def is_active(self) -> bool:
        '''
            Checks whether active cycle signal flag is set.

            :return: True if active flag is set, False otherwise.
        '''
