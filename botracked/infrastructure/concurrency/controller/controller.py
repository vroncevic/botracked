# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Provides LoopController adapter implementing ILoopController structurally.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.core.service.concurrency.irunner import IThreadRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LoopController:
    '''
        Defines class LoopController implementing ILoopController structurally.
        Coordinates consistent start, restart, and idle-safe stop of runnable loops.

        It defines:

            :attributes:
                | _runner - Concurrency thread runner port managing worker cycles.
                | _stop_flag - Signal flag notifying loop termination.
            :methods:
                | __init__ - Initializes controller with runner and stop flag.
                | start - Stops active cycle if needed and activates runnable loop.
                | stop - Signals loop stop and deactivates runner only when active.
                | is_running - Checks whether runner cycle is currently active.
                | __str__ - Returns string representation of loop controller.
    '''

    _runner: IThreadRunner
    _stop_flag: ISignalFlag

    def __init__(
        self,
        *,
        runner: IThreadRunner,
        stop_flag: ISignalFlag,
    ) -> None:
        '''
            Initializes loop controller with thread runner and stop signal flag.

            :param runner: Concurrency thread runner port.
            :param stop_flag: Signal flag notifying runnable loop termination.
            :exceptions: None.
        '''
        self._runner = runner
        self._stop_flag = stop_flag

    def start(self, worker: IRunnableWorker) -> None:
        '''
            Stops any active cycle, clears stop signal, and activates worker.

            :param worker: Runnable loop worker instance to execute.
            :exceptions: None.
        '''
        if self._runner.is_active():
            self.stop()

        self._stop_flag.clear()
        self._runner.activate(worker)

    def stop(self) -> None:
        '''
            Signals loop stop flag and deactivates active runner cycle if running.

            :exceptions: None.
        '''
        self._stop_flag.set()

        if self._runner.is_active():
            self._runner.deactivate()

    def is_running(self) -> bool:
        '''
            Checks whether background loop execution cycle is currently active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return self._runner.is_active()

    def __str__(self) -> str:
        '''
            Returns string representation of loop controller adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
