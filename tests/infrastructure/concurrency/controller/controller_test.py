# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit tests for LoopController background lifecycle adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.concurrency.irunnable import IRunnableWorker
from botracked.core.service.concurrency.irunner import IThreadRunner
from botracked.infrastructure.concurrency.controller.controller import LoopController

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LoopControllerTest(TestCase):
    '''
        Verifies LoopController idle-safe start, restart, stop, and status.
    '''

    def test_idle_start_restart_and_idle_safe_stop(self) -> None:
        '''
            Verifies LoopController avoids deactivate when idle and restarts cleanly.

            :exceptions: None.
        '''
        runner = Mock(spec=IThreadRunner)
        stop_flag = Mock(spec=ISignalFlag)
        worker = Mock(spec=IRunnableWorker)
        ctrl = LoopController(runner=runner, stop_flag=stop_flag)

        runner.is_active.return_value = False
        self.assertFalse(ctrl.is_running())
        ctrl.stop()
        stop_flag.set.assert_called_once()
        runner.deactivate.assert_not_called()

        ctrl.start(worker)
        stop_flag.clear.assert_called_once()
        runner.activate.assert_called_once_with(worker)
        runner.deactivate.assert_not_called()

        runner.is_active.return_value = True
        self.assertTrue(ctrl.is_running())
        ctrl.start(worker)
        runner.deactivate.assert_called_once()
        self.assertEqual(runner.activate.call_count, 2)
        self.assertIn('LoopController', str(ctrl))


if __name__ == '__main__':
    main()
