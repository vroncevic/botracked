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
    Defines factory creating data reception task provisions.
'''

from __future__ import annotations

from botracked.core.service.connection.receiver.dependencies import ReceiverDependencies
from botracked.core.service.connection.receiver.provides import ReceiverProvides
from botracked.core.service.connection.receiver.task import ReceptionTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReceiverFactory:
    '''
        Defines class ReceiverFactory with classmethod(s).
        Factory creating reception task provisions without foreign factory coupling.

        It defines:

            :methods:
                | create - Instantiates and encapsulates reception task.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(cls, dependencies: ReceiverDependencies) -> ReceiverProvides:
        '''
            Instantiates and encapsulates reception task.

            :param dependencies: Parameter bundle with receiver configuration.
            :return: Provisions container with receiver and worker task interfaces.
            :exceptions: None.
        '''
        task: ReceptionTask = ReceptionTask(
            reader=dependencies.reader,
            queue=dependencies.queue,
            buffer_size=dependencies.buffer_size,
        )
        return ReceiverProvides(receiver=task, worker_task=task)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
