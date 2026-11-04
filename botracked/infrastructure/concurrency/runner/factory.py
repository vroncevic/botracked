# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines ThreadRunnerFactory assembling ThreadRunner over stdlib primitives.
'''

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from threading import Event
from typing import ClassVar

from botracked.infrastructure.concurrency.runner.cycle.cycle import RunnerCycle
from botracked.infrastructure.concurrency.runner.dependencies import ThreadRunnerDependencies
from botracked.infrastructure.concurrency.runner.provides import ThreadRunnerProvides
from botracked.infrastructure.concurrency.runner.runner import ThreadRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThreadRunnerFactory:
    '''
        Defines class ThreadRunnerFactory assembling ThreadRunner subsystem.

        It defines:

            :attributes:
                | MAX_WORKERS - Single dedicated background thread per runner.
            :methods:
                | create - Creates ThreadRunnerProvides from ThreadRunnerDependencies.
                | get_version - Returns factory version string.
    '''

    MAX_WORKERS: ClassVar[int] = 1

    @classmethod
    def create(cls, dependencies: ThreadRunnerDependencies) -> ThreadRunnerProvides:
        '''
            Creates ThreadRunnerProvides from ThreadRunnerDependencies.

            :param dependencies: Configuration bundle with thread name and join timeout.
            :return: Assembled ThreadRunnerProvides bundle.
            :exceptions: None.
        '''
        executor = ThreadPoolExecutor(
            max_workers=cls.MAX_WORKERS,
            thread_name_prefix=dependencies.thread_name,
        )
        active_flag = Event()
        stopped_flag = Event()
        stopped_flag.set()
        cycle = RunnerCycle(
            active_flag=active_flag,
            stopped_flag=stopped_flag,
        )
        runner = ThreadRunner(
            executor=executor,
            cycle=cycle,
            join_timeout=dependencies.join_timeout,
        )

        return ThreadRunnerProvides(runner=runner)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
