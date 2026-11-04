# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Defines BotServiceFactory assembling core robot application services bundle.
'''

from __future__ import annotations

from typing import ClassVar

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.core.service.bundle.services import BotServicesBundle
from botracked.core.service.connection.dispatcher.dependencies import FrameDispatcherDependencies
from botracked.core.service.connection.dispatcher.factory import FrameDispatcherFactory
from botracked.infrastructure.codec.crc.dependencies import CrcDependencies
from botracked.infrastructure.codec.crc.factory import CrcFactory
from botracked.infrastructure.codec.dependencies import CodecDependencies
from botracked.infrastructure.codec.factory import CodecFactory
from botracked.infrastructure.concurrency.clock.factory import ClockFactory
from botracked.setup.service.connection import ConnectionAssembler
from botracked.setup.service.dsl import DslAssembler
from botracked.setup.service.mission import MissionAssembler
from botracked.setup.service.motion import MotionAssembler
from botracked.setup.service.telemetry import TelemetryAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotServiceFactory:
    '''
        Defines class BotServiceFactory with attribute(s) and method(s).
        Assembles all collaborator services and runners into BotRuntimeBundle.

        It defines:

            :attributes:
                | CRC_POLYNOMIAL - CRC-8 ATM/SMBus generator polynomial.
            :methods:
                | create - Assembles and returns wired BotRuntimeBundle instance.
                | get_version - Returns factory version string.
    '''

    CRC_POLYNOMIAL: ClassVar[int] = 0x07

    @classmethod
    def create(cls) -> BotRuntimeBundle:
        '''
            Assembles and returns wired BotRuntimeBundle instance.

            :return: Fully configured BotRuntimeBundle instance.
            :exceptions: None.
        '''
        clock = ClockFactory.create().clock
        codec = CodecFactory.create(
            CodecDependencies(
                crc_calculator=CrcFactory.create(
                    CrcDependencies(polynomial=cls.CRC_POLYNOMIAL)
                ).calculator
            )
        ).codec

        conn_prov = ConnectionAssembler.assemble()
        telem_prov = TelemetryAssembler.assemble_service()

        dispatcher = FrameDispatcherFactory.create(
            FrameDispatcherDependencies(
                codec=codec,
                transmitter=conn_prov.transmitter,
                status=conn_prov.port_status,
                sink=telem_prov.sink,
            )
        ).dispatcher

        motion_prov = MotionAssembler.assemble(dispatcher)
        dsl_service = DslAssembler.assemble(codec)

        listener = TelemetryAssembler.assemble_listener(
            receiver=conn_prov.receiver,
            codec=codec,
            sink=telem_prov.sink,
            clock=clock,
        )
        poller = TelemetryAssembler.assemble_poller(dispatcher=dispatcher)
        mission_runner = MissionAssembler.assemble(
            clock=clock, actuator=motion_prov.actuator
        )

        return BotRuntimeBundle(
            services=BotServicesBundle(
                connection=conn_prov.service,
                motion=motion_prov.service,
                telemetry=telem_prov.service,
                dsl=dsl_service,
            ),
            runners=BotRunnersBundle(
                listener=listener,
                poller=poller,
                mission=mission_runner,
            ),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
