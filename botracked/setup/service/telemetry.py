# -*- coding: UTF-8 -*-

'''
Module
    telemetry.py
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
    Defines TelemetryAssembler assembling telemetry service, listener, and poller.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.connection.dispatcher.idispatcher import IFrameDispatcher
from botracked.core.service.connection.receiver.protocol.ireceiver import IByteReceiver
from botracked.core.service.telemetry.factory import TelemetryServiceFactory
from botracked.core.service.telemetry.inspector.dependencies import TelemetryInspectorDependencies
from botracked.core.service.telemetry.inspector.factory import TelemetryInspectorFactory
from botracked.core.service.telemetry.listener.dependencies import TelemetryListenerDependencies
from botracked.core.service.telemetry.listener.factory import TelemetryListenerFactory
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.dependencies import TelemetryPollerDependencies
from botracked.core.service.telemetry.poller.factory import TelemetryPollerFactory
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink
from botracked.core.service.telemetry.provides import TelemetryServiceProvides
from botracked.infrastructure.concurrency.controller.dependencies import LoopControllerDependencies
from botracked.infrastructure.concurrency.controller.factory import LoopControllerFactory
from botracked.infrastructure.concurrency.flag.factory import SignalFlagFactory
from botracked.infrastructure.concurrency.runner.dependencies import ThreadRunnerDependencies
from botracked.infrastructure.concurrency.runner.factory import ThreadRunnerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryAssembler:
    '''
        Defines class TelemetryAssembler assembling telemetry subsystem.

        It defines:

            :attributes:
                | LISTENER_THREAD_NAME - Thread prefix for telemetry listener.
                | POLLER_THREAD_NAME - Thread prefix for telemetry poller.
                | RX_DEQUEUE_TIMEOUT - Inbound queue poll timeout in seconds.
                | POLLER_INTERVAL_SEC - Periodic status poll interval in seconds.
                | WORKER_JOIN_TIMEOUT - Thread runner shutdown timeout in seconds.
            :methods:
                | assemble_service - Instantiates telemetry service and sink.
                | assemble_listener - Wires listener runner for telemetry.
                | assemble_poller - Wires poller runner for telemetry.
                | get_version - Returns assembler version string.
    '''

    LISTENER_THREAD_NAME: ClassVar[str] = 'TelemetryListener'
    POLLER_THREAD_NAME: ClassVar[str] = 'TelemetryPoller'
    RX_DEQUEUE_TIMEOUT: ClassVar[float] = 0.05
    POLLER_INTERVAL_SEC: ClassVar[float] = 0.5
    WORKER_JOIN_TIMEOUT: ClassVar[float] = 0.5

    @classmethod
    def assemble_service(cls) -> TelemetryServiceProvides:
        '''
            Instantiates telemetry service and sink provider.

            :return: TelemetryServiceProvides instance.
            :exceptions: None.
        '''
        return TelemetryServiceFactory.create()

    @classmethod
    def assemble_listener(
        cls,
        *,
        receiver: IByteReceiver,
        codec: IBinaryCodec,
        sink: ITelemetrySink,
        clock: IClock,
    ) -> ITelemetryListener:
        '''
            Wires telemetry listener background thread runner.

            :param receiver: Inbound byte reception port.
            :param codec: Binary codec port.
            :param sink: Inbound packet observer sink.
            :param clock: Monotonic clock port.
            :return: Configured ITelemetryListener instance.
            :exceptions: None.
        '''
        listener_flag = SignalFlagFactory.create().flag
        return TelemetryListenerFactory.create(
            TelemetryListenerDependencies(
                receiver=receiver,
                codec=codec,
                inspector=TelemetryInspectorFactory.create(
                    TelemetryInspectorDependencies(clock=clock)
                ).inspector,
                sink=sink,
                clock=clock,
                controller=LoopControllerFactory.create(
                    LoopControllerDependencies(
                        runner=ThreadRunnerFactory.create(
                            ThreadRunnerDependencies(
                                thread_name=cls.LISTENER_THREAD_NAME,
                                join_timeout=cls.WORKER_JOIN_TIMEOUT,
                            )
                        ).runner,
                        stop_flag=listener_flag,
                    )
                ).controller,
                stop_flag=listener_flag,
                timeout_sec=cls.RX_DEQUEUE_TIMEOUT,
            )
        ).listener

    @classmethod
    def assemble_poller(
        cls, *, dispatcher: IFrameDispatcher
    ) -> ITelemetryPoller:
        '''
            Wires telemetry status poller background thread runner.

            :param dispatcher: Outbound command frame dispatcher port.
            :return: Configured ITelemetryPoller instance.
            :exceptions: None.
        '''
        poller_flag = SignalFlagFactory.create().flag
        return TelemetryPollerFactory.create(
            TelemetryPollerDependencies(
                dispatcher=dispatcher,
                controller=LoopControllerFactory.create(
                    LoopControllerDependencies(
                        runner=ThreadRunnerFactory.create(
                            ThreadRunnerDependencies(
                                thread_name=cls.POLLER_THREAD_NAME,
                                join_timeout=cls.WORKER_JOIN_TIMEOUT,
                            )
                        ).runner,
                        stop_flag=poller_flag,
                    )
                ).controller,
                stop_flag=poller_flag,
                interval_sec=cls.POLLER_INTERVAL_SEC,
            )
        ).poller

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
