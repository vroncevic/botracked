# -*- coding: UTF-8 -*-

'''
Module
    irunner.py
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
    Defines driven port IThreadRunner abstracting background concurrency execution.
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
class IThreadRunner(Protocol):
    '''
        Defines driven port IThreadRunner managing asynchronous worker execution.

        It defines:

            :methods:
                | activate - Marks cycle active and schedules worker execution.
                | deactivate - Clears active state and waits for cycle completion.
                | is_active - Checks whether worker execution cycle is active.
    '''

    def activate(self, worker: IRunnableWorker) -> None:
        '''
            Marks cycle active and schedules worker execution.

            :param worker: Runnable worker instance whose run loop will be executed.
        '''

    def deactivate(self) -> None:
        '''
            Clears active state and waits for cycle completion.
        '''

    def is_active(self) -> bool:
        '''
            Checks whether worker execution cycle is active.

            :return: True if active, False otherwise.
        '''
