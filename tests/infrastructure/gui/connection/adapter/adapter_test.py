# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for ConnectionActionAdapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.infrastructure.gui.connection.adapter.adapter import ConnectionActionAdapter
from botracked.infrastructure.gui.connection.adapter.dependencies import ConnectionAdapterDependencies
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionActionAdapterTest(TestCase):
    '''
        Tests ConnectionActionAdapter connect, disconnect, and port scanning.
    '''

    def test_connect_disconnect_and_ports(self) -> None:
        '''
            Verifies connect success/failure, disconnect, and port scan.

            :exceptions: None.
        '''
        conn = MagicMock(spec=IBotConnectionService)
        listener = MagicMock(spec=ITelemetryListener)
        poller = MagicMock(spec=ITelemetryPoller)
        mission = MagicMock(spec=IMissionRunner)
        scanner = MagicMock(spec=IPortScanner)
        scanner.scan_ports.return_value = ('/dev/ttyACM0',)
        logger = MagicMock(spec=ILogListener)

        adapter = ConnectionActionAdapter(
            ConnectionAdapterDependencies(
                connection_service=conn,
                listener=listener,
                poller=poller,
                mission_runner=mission,
                port_scanner=scanner,
                log_listener=logger,
            )
        )
        params = ConnectionParams(
            serial_port='/dev/ttyACM0', baud_rate=115200, timeout=1.0
        )
        ok, msg = adapter.handle_connect(params)
        self.assertTrue(ok)
        self.assertIn('Connected', msg)
        listener.start.assert_called_once()
        poller.start.assert_called_once()

        adapter.handle_disconnect()
        poller.stop.assert_called_once()
        listener.stop.assert_called_once()
        mission.abort.assert_called_once()
        conn.disconnect.assert_called_once()

        self.assertEqual(adapter.handle_refresh_ports(), ('/dev/ttyACM0',))
        self.assertTrue(adapter.has_available_ports())

        conn.connect.side_effect = BotConnectionError('busy')
        ok_fail, _ = adapter.handle_connect(params)
        self.assertFalse(ok_fail)


if __name__ == '__main__':
    main()
