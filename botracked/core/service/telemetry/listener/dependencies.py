# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines TelemetryListenerDependencies immutable collaborator bundle.
'''

from __future__ import annotations

from dataclasses import dataclass

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.concurrency.icontroller import ILoopController
from botracked.core.service.concurrency.iflag import ISignalFlag
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class TelemetryListenerDependencies:
    '''
        Parameter bundle grouping collaborators for TelemetryListenerFactory.

        It defines:

            :attributes:
                | receiver - Buffered inbound byte receiver port.
                | codec - Binary frame stream decoder port.
                | inspector - Telemetry payload field decoder port.
                | sink - Narrow sink broadcasting telemetry and packet events.
                | clock - Monotonic clock port computing elapsed uptime.
                | controller - Concurrency loop controller driving listener loop.
                | stop_flag - Signal flag notifying loop termination.
                | timeout_sec - Dequeue wait timeout duration in seconds.
    '''

    receiver: IByteReceiver
    codec: IBinaryCodec
    inspector: ITelemetryInspector
    sink: ITelemetrySink
    clock: IClock
    controller: ILoopController
    stop_flag: ISignalFlag
    timeout_sec: float
