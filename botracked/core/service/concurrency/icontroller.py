# -*- coding: UTF-8 -*-

'''
Module
    icontroller.py
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
    Defines driven port ILoopController managing background runnable lifecycles.
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
class ILoopController(Protocol):
    '''
        Defines driven port ILoopController coordinating runnable loop execution.

        It defines:

            :methods:
                | start - Restarts or activates background runnable loop cycle.
                | stop - Signals stop and deactivates active runner cycle.
                | is_running - Checks whether background runner cycle is active.
    '''

    def start(self, worker: IRunnableWorker) -> None:
        '''
            Stops any active cycle, clears stop signal, and activates worker.

            :param worker: Runnable loop worker instance to execute.
        '''

    def stop(self) -> None:
        '''
            Signals loop stop flag and deactivates active runner cycle if running.
        '''

    def is_running(self) -> bool:
        '''
            Checks whether background loop execution cycle is currently active.

            :return: True if active, False otherwise.
        '''
