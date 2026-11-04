# -*- coding: UTF-8 -*-

'''
Module
    telemetry_test.py
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
    Unit tests for TelemetryAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink
from botracked.core.service.telemetry.provides import TelemetryServiceProvides
from botracked.setup.service.telemetry import TelemetryAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryAssemblerTest(TestCase):
    '''
        Tests TelemetryAssembler service and runners wiring.
    '''

    def test_assemble_service(self) -> None:
        '''
            Verifies TelemetryAssembler service creation.

            :exceptions: None.
        '''
        prov: TelemetryServiceProvides = TelemetryAssembler.assemble_service()
        self.assertIsNotNone(prov.service)
        self.assertIsNotNone(prov.sink)

    def test_assemble_listener(self) -> None:
        '''
            Verifies TelemetryAssembler listener creation.

            :exceptions: None.
        '''
        listener: ITelemetryListener = TelemetryAssembler.assemble_listener(
            receiver=MagicMock(spec=IByteReceiver),
            codec=MagicMock(spec=IBinaryCodec),
            sink=MagicMock(spec=ITelemetrySink),
            clock=MagicMock(spec=IClock),
        )
        self.assertIsInstance(listener, ITelemetryListener)

    def test_assemble_poller(self) -> None:
        '''
            Verifies TelemetryAssembler poller creation.

            :exceptions: None.
        '''
        poller: ITelemetryPoller = TelemetryAssembler.assemble_poller(
            dispatcher=MagicMock(spec=IFrameDispatcher)
        )
        self.assertIsInstance(poller, ITelemetryPoller)
        self.assertEqual(TelemetryAssembler.POLLER_INTERVAL_SEC, 0.5)
        self.assertEqual(TelemetryAssembler.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
