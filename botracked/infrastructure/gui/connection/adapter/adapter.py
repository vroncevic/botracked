# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Provides ConnectionActionAdapter bridging GUI events to connection services.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.model.exceptions.connection_error import BotConnectionError
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
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


class ConnectionActionAdapter:
    '''
        Defines class ConnectionActionAdapter implementing
        IConnectionActionDelegate and IPortRefreshDelegate contracts.

        It defines:

            :attributes:
                | LEVEL_INFO - Informational log severity tag.
                | LEVEL_WARN - Warning log severity tag.
                | LEVEL_ERROR - Error log severity tag.
                | MSG_FAILED - Badge text returned when serial open fails.
                | _connection_service - Link connection management service.
                | _listener - Background inbound telemetry listener.
                | _poller - Background periodic telemetry poller.
                | _mission_runner - Asynchronous mission runner.
                | _port_scanner - Hardware serial port scanner port.
                | _log_listener - Diagnostic UI console log listener port.
            :methods:
                | __init__ - Initializes adapter with collaborator bundle.
                | handle_connect - Opens link, starts telemetry threads, logs state.
                | handle_disconnect - Stops telemetry threads, aborts, closes link.
                | handle_refresh_ports - Scans and returns detected serial ports.
                | has_available_ports - Checks if at least one port is detected.
    '''

    LEVEL_INFO: ClassVar[str] = 'INFO'
    LEVEL_WARN: ClassVar[str] = 'WARN'
    LEVEL_ERROR: ClassVar[str] = 'ERROR'
    MSG_FAILED: ClassVar[str] = 'Connection Failed'

    _connection_service: IBotConnectionService
    _listener: ITelemetryListener
    _poller: ITelemetryPoller
    _mission_runner: IMissionRunner
    _port_scanner: IPortScanner
    _log_listener: ILogListener

    def __init__(self, dependencies: ConnectionAdapterDependencies) -> None:
        '''
            Initializes adapter with core services, scanner, and log listener.

            :param dependencies: Connection adapter collaborator ports bundle.
            :exceptions: None.
        '''
        self._connection_service = dependencies.connection_service
        self._listener = dependencies.listener
        self._poller = dependencies.poller
        self._mission_runner = dependencies.mission_runner
        self._port_scanner = dependencies.port_scanner
        self._log_listener = dependencies.log_listener

    def handle_connect(self, params: ConnectionParams) -> tuple[bool, str]:
        '''
            Initiates serial link connection, starts listener/poller, and logs.

            :param params: Connection configuration parameters.
            :return: Tuple of connection boolean state and badge label string.
            :exceptions: None.
        '''
        try:
            self._connection_service.connect(params)
            self._listener.start()
            self._poller.start()
            self._log_listener.write_entry(
                self.LEVEL_INFO,
                f'Connected to {params.serial_port} @ {params.baud_rate} baud',
            )
            return (True, f'Connected ({params.serial_port})')

        except BotConnectionError as exc:
            self._log_listener.write_entry(
                self.LEVEL_ERROR, f'Serial connect failed: {exc}'
            )
            return (False, self.MSG_FAILED)

    def handle_disconnect(self) -> None:
        '''
            Stops telemetry poller/listener, aborts missions, and closes link.

            :exceptions: None.
        '''
        self._poller.stop()
        self._listener.stop()
        self._mission_runner.abort()
        self._connection_service.disconnect()
        self._log_listener.write_entry(
            self.LEVEL_WARN, 'Disconnected serial link'
        )

    def handle_refresh_ports(self) -> tuple[str, ...]:
        '''
            Scans and retrieves available serial ports.

            :return: Tuple of detected port device path strings.
            :exceptions: None.
        '''
        return tuple(self._port_scanner.scan_ports())

    def has_available_ports(self) -> bool:
        '''
            Checks whether at least one serial port is currently detected.

            :return: True if ports exist, False otherwise.
            :exceptions: None.
        '''
        return bool(self.handle_refresh_ports())
