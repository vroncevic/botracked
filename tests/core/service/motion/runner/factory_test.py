# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for MissionRunnerFactory subsystem assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.motion.runner.dependencies import MissionRunnerDependencies
from botracked.core.service.motion.runner.factory import MissionRunnerFactory
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.motion.runner.worker.iworker import IMissionExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MissionRunnerFactoryTest(TestCase):
    '''
        Verifies MissionRunnerFactory creation and version reporting.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies MissionRunnerFactory returns IMissionRunner provider.

            :exceptions: None.
        '''
        prov = MissionRunnerFactory.create(
            MissionRunnerDependencies(
                worker=Mock(spec=IMissionExecutionWorker),
                controller=Mock(spec=ILoopController),
                pause_flag=Mock(spec=ISignalFlag),
            )
        )
        self.assertIsInstance(prov.runner, IMissionRunner)
        self.assertEqual(MissionRunnerFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
