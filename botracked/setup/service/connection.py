# -*- coding: UTF-8 -*-

'''
Module
    connection.py
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
    Defines ConnectionAssembler wiring serial communication pipeline.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.connection.dependencies import ConnectionServiceDependencies
from botracked.core.service.connection.factory import ConnectionServiceFactory
from botracked.core.service.connection.receiver.dependencies import ReceiverDependencies as ReceiverServiceDependencies
from botracked.core.service.connection.receiver.factory import ReceiverFactory as ReceiverServiceFactory
from botracked.core.service.connection.transmitter.dependencies import TransmitterDependencies as TransmitterServiceDependencies
from botracked.core.service.connection.transmitter.factory import TransmitterFactory as TransmitterServiceFactory
from botracked.core.service.connection.worker.dependencies import WorkerDependencies
from botracked.core.service.connection.worker.factory import WorkerFactory
from botracked.infrastructure.concurrency.controller.dependencies import LoopControllerDependencies
from botracked.infrastructure.concurrency.controller.factory import LoopControllerFactory
from botracked.infrastructure.concurrency.flag.factory import SignalFlagFactory
from botracked.infrastructure.concurrency.runner.dependencies import ThreadRunnerDependencies
from botracked.infrastructure.concurrency.runner.factory import ThreadRunnerFactory
from botracked.infrastructure.connection.buffer.dependencies import ByteQueueDependencies
from botracked.infrastructure.connection.buffer.factory import ByteQueueFactory
from botracked.infrastructure.connection.driver.dependencies import DriverDependencies
from botracked.infrastructure.connection.driver.factory import DriverFactory
from botracked.infrastructure.connection.port.dependencies import PortDependencies
from botracked.infrastructure.connection.port.factory import PortFactory
from botracked.infrastructure.connection.receiver.dependencies import ReceiverDependencies as ReceiverInfraDependencies
from botracked.infrastructure.connection.receiver.factory import ReceiverFactory as ReceiverInfraFactory
from botracked.infrastructure.connection.transmitter.dependencies import TransmitterDependencies as TransmitterInfraDependencies
from botracked.infrastructure.connection.transmitter.factory import TransmitterFactory as TransmitterInfraFactory
from botracked.setup.service.connection_provides import ConnectionAssemblerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionAssembler:
    '''
        Defines class ConnectionAssembler wiring serial communication pipeline.

        It defines:

            :attributes:
                | PORT_TIMEOUT - Default serial read/write timeout in seconds.
                | INTER_BYTE_TIMEOUT - Inter-byte burst timeout in seconds or None.
                | TX_QUEUE_MAX_SIZE - Outgoing byte queue capacity (0 unbounded).
                | RX_QUEUE_MAX_SIZE - Inbound byte queue capacity (0 unbounded).
                | TX_DEQUEUE_TIMEOUT - Outgoing queue poll timeout in seconds.
                | RX_BUFFER_SIZE - Inbound serial chunk buffer size in bytes.
                | WORKER_JOIN_TIMEOUT - Thread runner shutdown timeout in seconds.
                | TX_THREAD_NAME - Thread prefix for transmission worker.
                | RX_THREAD_NAME - Thread prefix for reception worker.
            :methods:
                | assemble - Wires drivers, queues, workers, and returns ports.
                | get_version - Returns assembler version string.
    '''

    PORT_TIMEOUT: ClassVar[float] = 0.1
    INTER_BYTE_TIMEOUT: ClassVar[float | None] = None
    TX_QUEUE_MAX_SIZE: ClassVar[int] = 0
    RX_QUEUE_MAX_SIZE: ClassVar[int] = 0
    TX_DEQUEUE_TIMEOUT: ClassVar[float] = 0.05
    RX_BUFFER_SIZE: ClassVar[int] = 1024
    WORKER_JOIN_TIMEOUT: ClassVar[float] = 0.5
    TX_THREAD_NAME: ClassVar[str] = 'TransmissionWorker'
    RX_THREAD_NAME: ClassVar[str] = 'ReceptionWorker'

    @classmethod
    def assemble(cls) -> ConnectionAssemblerProvides:
        '''
            Wires drivers, queues, workers, and returns connection ports.

            :return: Assembled ConnectionAssemblerProvides bundle.
            :exceptions: None.
        '''
        driver_prov = DriverFactory.create(
            DriverDependencies(
                timeout=cls.PORT_TIMEOUT,
                inter_byte_timeout=cls.INTER_BYTE_TIMEOUT,
            )
        )
        port_prov = PortFactory.create(
            PortDependencies(driver=driver_prov.driver)
        )
        tx_srv_prov = TransmitterServiceFactory.create(
            TransmitterServiceDependencies(
                writer=TransmitterInfraFactory.create(
                    TransmitterInfraDependencies(driver=driver_prov.driver)
                ).writer,
                queue=ByteQueueFactory.create(
                    ByteQueueDependencies(max_size=cls.TX_QUEUE_MAX_SIZE)
                ).queue,
                timeout=cls.TX_DEQUEUE_TIMEOUT,
            )
        )
        rx_srv_prov = ReceiverServiceFactory.create(
            ReceiverServiceDependencies(
                reader=ReceiverInfraFactory.create(
                    ReceiverInfraDependencies(driver=driver_prov.driver)
                ).reader,
                queue=ByteQueueFactory.create(
                    ByteQueueDependencies(max_size=cls.RX_QUEUE_MAX_SIZE)
                ).queue,
                buffer_size=cls.RX_BUFFER_SIZE,
            )
        )
        rx_flag = SignalFlagFactory.create().flag
        tx_flag = SignalFlagFactory.create().flag

        conn_service = ConnectionServiceFactory.create(
            ConnectionServiceDependencies(
                port=port_prov.port,
                receiver_worker=WorkerFactory.create(
                    WorkerDependencies(
                        task=rx_srv_prov.worker_task,
                        controller=LoopControllerFactory.create(
                            LoopControllerDependencies(
                                runner=ThreadRunnerFactory.create(
                                    ThreadRunnerDependencies(
                                        thread_name=cls.RX_THREAD_NAME,
                                        join_timeout=cls.WORKER_JOIN_TIMEOUT,
                                    )
                                ).runner,
                                stop_flag=rx_flag,
                            )
                        ).controller,
                        stop_flag=rx_flag,
                    )
                ).worker,
                transmitter_worker=WorkerFactory.create(
                    WorkerDependencies(
                        task=tx_srv_prov.worker_task,
                        controller=LoopControllerFactory.create(
                            LoopControllerDependencies(
                                runner=ThreadRunnerFactory.create(
                                    ThreadRunnerDependencies(
                                        thread_name=cls.TX_THREAD_NAME,
                                        join_timeout=cls.WORKER_JOIN_TIMEOUT,
                                    )
                                ).runner,
                                stop_flag=tx_flag,
                            )
                        ).controller,
                        stop_flag=tx_flag,
                    )
                ).worker,
            )
        ).service

        return ConnectionAssemblerProvides(
            service=conn_service,
            port_status=port_prov.status,
            transmitter=tx_srv_prov.transmitter,
            receiver=rx_srv_prov.receiver,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
