# -*- coding: UTF-8 -*-

'''
Module
    task_test.py
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
    Unit tests for WorkerTask fault containment and idempotent cleanup.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.service.connection.worker.task.itask import IWorkerTask
from botracked.core.service.connection.worker.task.task import WorkerTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerTaskTest(TestCase):
    '''
        Verifies WorkerTask error containment and idempotent cleanup.
    '''

    def test_execute_step_and_idempotent_cleanup(self) -> None:
        '''
            Verifies BotConnectionError returns False and cleanup runs once per cycle.

            :exceptions: None.
        '''
        inner = Mock(spec=IWorkerTask)
        inner.execute_step.side_effect = [True, BotConnectionError('lost'), True]
        guarded = WorkerTask(inner)

        self.assertTrue(guarded.execute_step())
        self.assertFalse(guarded.execute_step())

        guarded.cleanup()
        guarded.cleanup()
        inner.cleanup.assert_called_once()

        self.assertTrue(guarded.execute_step())
        guarded.cleanup()
        self.assertEqual(inner.cleanup.call_count, 2)


if __name__ == '__main__':
    main()
