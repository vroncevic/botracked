# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Defines test cases for BotConnectionService.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.service.connection.port.iport import IConnectionPort
from botracked.core.service.connection.service import BotConnectionService
from botracked.core.service.connection.worker.iworker import IConnectionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotConnectionServiceTestCase(TestCase):
    '''
        Defines test methods for BotConnectionService behavior.
    '''

    def setUp(self) -> None:
        '''
            Prepares test fixtures.

            :exceptions: None.
        '''
        self.mock_port = Mock(spec=IConnectionPort)
        self.mock_port.is_connected.return_value = False
        self.mock_rcv_worker = Mock(spec=IConnectionWorker)
        self.mock_tx_worker = Mock(spec=IConnectionWorker)

        self.service = BotConnectionService(
            port=self.mock_port,
            receiver_worker=self.mock_rcv_worker,
            transmitter_worker=self.mock_tx_worker,
        )
        self.params = ConnectionParams(
            serial_port='/dev/ttyUSB0',
            baud_rate=115200,
            timeout=1.0,
        )

    def test_initial_state(self) -> None:
        '''
            Verifies initial disconnected status of connection service.

            :exceptions: None.
        '''
        self.assertFalse(self.service.is_connected())

    def test_connect_success(self) -> None:
        '''
            Verifies successful connection starts workers and opens port.

            :exceptions: None.
        '''
        self.mock_port.connect.return_value = True
        self.mock_port.is_connected.return_value = True
        self.assertTrue(self.service.connect(self.params))
        self.assertTrue(self.service.is_connected())
        self.mock_port.connect.assert_called_once_with('/dev/ttyUSB0', 115200)
        self.mock_rcv_worker.start.assert_called_once()
        self.mock_tx_worker.start.assert_called_once()

    def test_connect_failure(self) -> None:
        '''
            Verifies failed port open prevents worker startup.

            :exceptions: None.
        '''
        self.mock_port.connect.return_value = False
        self.mock_port.is_connected.return_value = False
        self.assertFalse(self.service.connect(self.params))
        self.mock_rcv_worker.start.assert_not_called()
        self.mock_tx_worker.start.assert_not_called()

    def test_disconnect_and_reconnect_cleanup(self) -> None:
        '''
            Verifies disconnect stops workers and closes port.

            :exceptions: None.
        '''
        self.mock_port.connect.return_value = True
        self.service.connect(self.params)
        self.service.disconnect()
        self.mock_rcv_worker.stop.assert_called()
        self.mock_tx_worker.stop.assert_called()
        self.mock_port.disconnect.assert_called()


if __name__ == '__main__':
    main()
