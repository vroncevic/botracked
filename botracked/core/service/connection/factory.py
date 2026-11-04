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
    Defines factory creating BotConnectionService provisions.
'''

from __future__ import annotations

from botracked.core.service.connection.dependencies import ConnectionServiceDependencies
from botracked.core.service.connection.provides import ConnectionServiceProvides
from botracked.core.service.connection.service import BotConnectionService

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionServiceFactory:
    '''
        Defines class ConnectionServiceFactory with classmethod(s).
        Factory creating BotConnectionService provisions.

        It defines:

            :methods:
                | create - Instantiates and encapsulates connection service.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(
        cls, dependencies: ConnectionServiceDependencies
    ) -> ConnectionServiceProvides:
        '''
            Instantiates and encapsulates connection service.

            :param dependencies: Parameter bundle with connection collaborators.
            :return: Provisions container with connection service interface.
            :exceptions: None.
        '''
        service: BotConnectionService = BotConnectionService(
            port=dependencies.port,
            receiver_worker=dependencies.receiver_worker,
            transmitter_worker=dependencies.transmitter_worker,
        )

        return ConnectionServiceProvides(service=service)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
