# -*- coding: UTF-8 -*-

'''
Module
    connection_provides_test.py
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
    Unit tests for ConnectionAssemblerProvides.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.connection.port.istatus import IConnectionStatus
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.connection.transmitter.protocol.itransmitter import IByteTransmitter
from botracked.setup.service.connection_provides import ConnectionAssemblerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionAssemblerProvidesTest(TestCase):
    '''
        Tests ConnectionAssemblerProvides output bundle fields.
    '''

    def test_fields(self) -> None:
        '''
            Verifies port retention on ConnectionAssemblerProvides.

            :exceptions: None.
        '''
        service = MagicMock(spec=IBotConnectionService)
        status = MagicMock(spec=IConnectionStatus)
        tx = MagicMock(spec=IByteTransmitter)
        rx = MagicMock(spec=IByteReceiver)

        prov = ConnectionAssemblerProvides(
            service=service,
            port_status=status,
            transmitter=tx,
            receiver=rx,
        )
        self.assertIs(prov.service, service)
        self.assertIs(prov.port_status, status)
        self.assertIs(prov.transmitter, tx)
        self.assertIs(prov.receiver, rx)


if __name__ == '__main__':
    main()
