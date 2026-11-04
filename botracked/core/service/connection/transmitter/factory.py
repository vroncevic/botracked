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
    Defines factory creating data transmission task provisions.
'''

from __future__ import annotations

from botracked.core.service.connection.transmitter.dependencies import TransmitterDependencies
from botracked.core.service.connection.transmitter.provides import TransmitterProvides
from botracked.core.service.connection.transmitter.task import TransmissionTask

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmitterFactory:
    '''
        Defines class TransmitterFactory with classmethod(s).
        Factory creating transmission task provisions without foreign factory coupling.

        It defines:

            :methods:
                | create - Instantiates and encapsulates transmission task.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(
        cls, dependencies: TransmitterDependencies
    ) -> TransmitterProvides:
        '''
            Instantiates and encapsulates transmission task.

            :param dependencies: Parameter bundle with transmitter configuration.
            :return: Provisions container with transmitter and worker task interfaces.
            :exceptions: None.
        '''
        task: TransmissionTask = TransmissionTask(
            writer=dependencies.writer,
            queue=dependencies.queue,
            timeout=dependencies.timeout,
        )
        return TransmitterProvides(transmitter=task, worker_task=task)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
