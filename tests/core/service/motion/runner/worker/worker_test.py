# -*- coding: UTF-8 -*-

'''
Module
    worker_test.py
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
    Unit tests for MissionExecutionWorker.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.dsl.compiled_step import CompiledStep
from botracked.core.service.motion.protocol.iactuator import IMissionActuator
from botracked.core.service.motion.runner.pacer.ipacer import IMissionPacer
from botracked.core.service.motion.runner.worker.worker import MissionExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionExecutionWorkerTestCase(TestCase):
    '''
        Verifies MissionExecutionWorker sequential step execution and abort.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.pacer = Mock(spec=IMissionPacer)
        self.motion = Mock(spec=IMissionActuator)
        self.stop_flag = Event()
        self.worker = MissionExecutionWorker(
            pacer=self.pacer,
            actuator=self.motion,
            stop_flag=self.stop_flag,
        )
        self.step = CompiledStep(
            frames=(b'\x01',),
            duration_sec=0.1,
            auto_stop_after=True,
            description='MOVE',
            line_number=1,
        )

    def test_load_run_and_execute_paths(self) -> None:
        '''
            Verifies load_steps, run execution, auto_stop, and interruptions.

            :exceptions: None.
        '''
        self.pacer.wait_paused.return_value = True
        self.pacer.sleep_step.return_value = True

        self.worker.load_steps([self.step])
        self.worker.run()
        self.assertEqual(self.motion.stop_motors.call_count, 2)
        self.assertFalse(self.worker.is_stopped())

        self.pacer.sleep_step.return_value = False
        self.assertFalse(self.worker.execute([self.step]))

        self.stop_flag.set()
        self.assertTrue(self.worker.is_stopped())
        self.assertFalse(self.worker.execute([self.step]))


if __name__ == '__main__':
    main()
