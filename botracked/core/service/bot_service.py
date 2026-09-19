# -*- coding: UTF-8 -*-

'''
Module
    bot_service.py
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
    Provides BotService facade orchestrating communications, telemetry, and missions.
'''

from __future__ import annotations

from botracked.core.model.connection_params import ConnectionParams
from botracked.core.model.telemetry_data import TelemetryData
from botracked.core.service.bot_motion_service import BotMotionService
from botracked.core.service.bot_telemetry_service import BotTelemetryService
from botracked.infrastructure.communication.binary_codec import BinaryCodec
from botracked.core.service.telemetry_poller import TelemetryPoller
from botracked.core.service.mission_runner import MissionRunner
from botracked.infrastructure.communication.serial_transport import SerialTransport
from botracked.infrastructure.communication.tcp_transport import TcpTransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotService:
    '''
        Defines class BotService with attribute(s) and method(s).
        Application interactor coordinating robot communications, telemetry, and missions.

        It defines:

            :attributes:
                | _codec - Binary frame encoder/decoder.
                | _serial_transport - Dedicated serial transport instance.
                | _tcp_transport - Dedicated TCP transport instance.
                | _active_transport - Currently active transport instance or None.
                | _motion_service - Controller service for kinematics and actuation.
                | _telemetry_service - Service for telemetry data and observer dispatch.
                | _poller - Background telemetry polling worker.
                | _mission_runner - Background mission script execution runner.
            :methods:
                | __init__ - Initializes bot service with transports and sub-services.
                | _get_active_transport - Returns active transport instance.
                | _on_telemetry_rx - Handles incoming telemetry from background receiver.
                | is_initialized - Checks if service is ready.
                | connect - Establishes communication link with robot.
                | disconnect - Disconnects active transport and stops background polling.
                | is_connected - Checks connection status.
                | get_motion - Returns active motion and actuation service.
                | get_telemetry - Returns active telemetry and observer service.
                | get_mission_runner - Returns background mission execution worker.
    '''

    _codec: BinaryCodec
    _serial_transport: SerialTransport
    _tcp_transport: TcpTransport
    _active_transport: SerialTransport | TcpTransport | None
    _motion_service: BotMotionService
    _telemetry_service: BotTelemetryService
    _poller: TelemetryPoller
    _mission_runner: MissionRunner

    def __init__(self) -> None:
        '''
            Initializes bot service with transports, codec, and sub-services.

            :exceptions: None.
        '''
        self._codec = BinaryCodec()
        self._serial_transport = SerialTransport()
        self._tcp_transport = TcpTransport()
        self._active_transport = None

        self._telemetry_service = BotTelemetryService(
            codec=self._codec,
            transport_provider=self._get_active_transport,
        )
        self._motion_service = BotMotionService(
            codec=self._codec,
            transport_provider=self._get_active_transport,
            on_tx=self._telemetry_service.notify_packet,
        )
        self._poller = TelemetryPoller(
            codec=self._codec,
            on_telemetry=self._on_telemetry_rx,
            on_packet=self._telemetry_service.notify_packet,
            request_status_fn=self._telemetry_service.request_status,
        )
        self._mission_runner = MissionRunner(
            execute_fn=self._motion_service.execute_step,
            stop_fn=self._motion_service.stop_motors,
        )

    def _get_active_transport(self) -> SerialTransport | TcpTransport | None:
        '''
            Returns active transport instance.

            :return: Connected transport or None.
            :exceptions: None.
        '''
        return self._active_transport

    def _on_telemetry_rx(self, data: TelemetryData) -> None:
        '''
            Handles incoming telemetry from background receiver.

            :param data: Decoded TelemetryData.
            :exceptions: None.
        '''
        self._telemetry_service.notify_telemetry(data)

    def is_initialized(self) -> bool:
        '''
            Checks if service is ready.

            :return: True always.
            :exceptions: None.
        '''
        return True

    def connect(self, params: ConnectionParams) -> bool:
        '''
            Establishes communication link with robot.

            :param params: Target connection parameters.
            :return: True if connected successfully, False otherwise.
            :exceptions: None.
        '''
        self.disconnect()

        if params.is_serial:
            self._active_transport = self._serial_transport
        else:
            self._active_transport = self._tcp_transport

        connected = self._active_transport.connect(params)

        if connected:
            self._poller.start(self._active_transport)
            self._telemetry_service.notify_connection_state(True, 'Connected')
        else:
            self._telemetry_service.notify_connection_state(
                False, 'Connection failed'
            )

        return connected

    def disconnect(self) -> None:
        '''
            Disconnects active transport and stops background polling.

            :exceptions: None.
        '''
        self._poller.stop()
        self._mission_runner.abort()

        if self._active_transport is not None:
            self._active_transport.disconnect()
            self._active_transport = None

        self._telemetry_service.notify_connection_state(False, 'Disconnected')

    def is_connected(self) -> bool:
        '''
            Checks connection status.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return (
            self._active_transport is not None
            and self._active_transport.is_connected()
        )

    def get_motion(self) -> BotMotionService:
        '''
            Returns active motion and actuation service.

            :return: BotMotionService instance.
            :exceptions: None.
        '''
        return self._motion_service

    def get_telemetry(self) -> BotTelemetryService:
        '''
            Returns active telemetry and observer service.

            :return: BotTelemetryService instance.
            :exceptions: None.
        '''
        return self._telemetry_service

    def get_mission_runner(self) -> MissionRunner:
        '''
            Returns background mission execution worker.

            :return: MissionRunner instance.
            :exceptions: None.
        '''
        return self._mission_runner
