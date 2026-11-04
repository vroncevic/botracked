# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Defines BotConnectionService orchestrating serial port and RX/TX workers.
'''

from __future__ import annotations

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.service.connection.port.iport import IConnectionPort
from botracked.core.service.connection.worker.iworker import IConnectionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotConnectionService:
    '''
        Defines class BotConnectionService managing port and worker lifecycles.
        Coordinates background reception and transmission workers over serial port.

        It defines:

            :attributes:
                | _port - Physical communication connection port adapter.
                | _receiver_worker - Background reception worker loop runner.
                | _transmitter_worker - Background transmission worker loop runner.
            :methods:
                | __init__ - Initializes connection service with collaborator ports.
                | connect - Connects communication port and starts workers.
                | disconnect - Stops workers and disconnects active port.
                | is_connected - Checks if communication port is open.
    '''

    _port: IConnectionPort
    _receiver_worker: IConnectionWorker
    _transmitter_worker: IConnectionWorker

    def __init__(
        self,
        *,
        port: IConnectionPort,
        receiver_worker: IConnectionWorker,
        transmitter_worker: IConnectionWorker,
    ) -> None:
        '''
            Initializes connection service with collaborator ports.

            :param port: Physical communication connection port adapter.
            :param receiver_worker: Background reception worker controller.
            :param transmitter_worker: Background transmission worker controller.
            :exceptions: None.
        '''
        self._port = port
        self._receiver_worker = receiver_worker
        self._transmitter_worker = transmitter_worker

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Connects communication port and starts workers.

            :param params: Connection configuration parameters.
            :return: True if successfully connected, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()
        connected: bool = self._port.connect(
            params.serial_port, params.baud_rate
        )

        if connected:
            self._receiver_worker.start()
            self._transmitter_worker.start()

        return connected

    def disconnect(self) -> None:
        '''
            Stops workers and disconnects active port.

            :exceptions: None.
        '''
        self._receiver_worker.stop()
        self._transmitter_worker.stop()
        self._port.disconnect()

    def is_connected(self) -> bool:
        '''
            Checks if communication port is open.

            :return: True if active port is open, False otherwise.
            :exceptions: None.
        '''
        return self._port.is_connected()
