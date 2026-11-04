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
    Defines factory creating background connection worker instances.
'''

from __future__ import annotations

from botracked.core.service.connection.worker.dependencies import WorkerDependencies
from botracked.core.service.connection.worker.loop.loop import WorkerLoop
from botracked.core.service.connection.worker.provides import WorkerProvides
from botracked.core.service.connection.worker.task.task import WorkerTask
from botracked.core.service.connection.worker.worker import ConnectionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerFactory:
    '''
        Defines class WorkerFactory with classmethod(s).
        Factory creating connection worker instances and provisions.

        It defines:

            :methods:
                | create - Instantiates and encapsulates connection worker.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(cls, dependencies: WorkerDependencies) -> WorkerProvides:
        '''
            Instantiates and encapsulates connection worker.

            :param dependencies: Parameter bundle with task, runner, and flag.
            :return: Provisions container with worker interface.
            :exceptions: None.
        '''
        guarded_task: WorkerTask = WorkerTask(dependencies.task)
        loop: WorkerLoop = WorkerLoop(
            task=guarded_task,
            stop_flag=dependencies.stop_flag,
        )
        worker: ConnectionWorker = ConnectionWorker(
            loop=loop,
            task=guarded_task,
            controller=dependencies.controller,
        )
        return WorkerProvides(worker=worker)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
