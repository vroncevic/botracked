# -*- coding: UTF-8 -*-

'''
Module
    irunnable_test.py
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
    Unit tests for IRunnableWorker structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.core.service.connection.worker.loop.loop import WorkerLoop
from botracked.core.service.connection.worker.task.itask import IWorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RunnableWorkerProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IRunnableWorker.
    '''

    def test_worker_loop_satisfies_runnable(self) -> None:
        '''
            Verifies WorkerLoop satisfies IRunnableWorker structurally.

            :exceptions: None.
        '''
        loop = WorkerLoop(
            task=Mock(spec=IWorkerTask),
            stop_flag=Mock(spec=ISignalFlag),
        )
        self.assertIsInstance(loop, IRunnableWorker)
        self.assertNotIsInstance('invalid', IRunnableWorker)


if __name__ == '__main__':
    main()
