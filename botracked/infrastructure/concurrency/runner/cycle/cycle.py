# -*- coding: UTF-8 -*-

'''
Module
    cycle.py
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
    Provides RunnerCycle action adapter managing background cycle flag cleanup.
'''

from __future__ import annotations

from ats_utilities.utils.reflection import to_str

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.concurrency.irunnable import IRunnableWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RunnerCycle:
    '''
        Defines class RunnerCycle implementing IRunnerCycle contract structurally.
        Encapsulates cycle lifecycle flags, worker execution, and stop synchronization.

        It defines:

            :attributes:
                | _active_flag - Signal flag tracking active loop execution state.
                | _stopped_flag - Signal flag notifying loop cycle termination.
            :methods:
                | __init__ - Initializes RunnerCycle with active and stopped flags.
                | prepare - Marks cycle active when currently idle.
                | __call__ - Runs worker and guarantees flag cleanup on completion.
                | stop - Clears active state and waits for cycle termination.
                | is_active - Checks whether active cycle signal flag is set.
                | __str__ - Returns string representation of cycle adapter.
    '''

    _active_flag: ISignalFlag
    _stopped_flag: ISignalFlag

    def __init__(
        self,
        *,
        active_flag: ISignalFlag,
        stopped_flag: ISignalFlag,
    ) -> None:
        '''
            Initializes RunnerCycle with active and stopped signal flags.

            :param active_flag: Event flag tracking active execution cycle.
            :param stopped_flag: Event flag signaling cycle completion.
            :exceptions: None.
        '''
        self._active_flag = active_flag
        self._stopped_flag = stopped_flag

    def prepare(self) -> bool:
        '''
            Marks cycle active when currently idle.

            :return: True if cycle transitioned to active, False if already active.
            :exceptions: None.
        '''
        if self._active_flag.is_set():
            return False

        self._stopped_flag.clear()
        self._active_flag.set()

        return True

    def __call__(self, worker: IRunnableWorker) -> None:
        '''
            Runs worker and guarantees flag cleanup upon completion or failure.

            :param worker: Runnable worker instance to execute on worker thread.
            :exceptions: None.
        '''
        try:
            worker.run()

        finally:
            self._active_flag.clear()
            self._stopped_flag.set()

    def stop(self, timeout: float) -> None:
        '''
            Clears active state and waits for cycle termination.

            :param timeout: Maximum wait duration in seconds.
            :exceptions: None.
        '''
        if self._active_flag.is_set():
            self._active_flag.clear()

        self._stopped_flag.wait(timeout)

    def is_active(self) -> bool:
        '''
            Checks whether active cycle signal flag is set.

            :return: True if active flag is set, False otherwise.
            :exceptions: None.
        '''
        return self._active_flag.is_set()

    def __str__(self) -> str:
        '''
            Returns string representation of cycle adapter.

            :return: String representation.
            :exceptions: None.
        '''
        return to_str(self)
