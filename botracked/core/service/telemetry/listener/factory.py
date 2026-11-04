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
    Defines TelemetryListenerFactory assembling decoder, loop, and listener.
'''

from __future__ import annotations

from botracked.core.service.telemetry.listener.decoder.decoder import TelemetryDecoder
from botracked.core.service.telemetry.listener.dependencies import TelemetryListenerDependencies
from botracked.core.service.telemetry.listener.listener import TelemetryListener
from botracked.core.service.telemetry.listener.loop.loop import TelemetryListenerLoop
from botracked.core.service.telemetry.listener.provides import TelemetryListenerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryListenerFactory:
    '''
        Defines class TelemetryListenerFactory assembling telemetry listener subsystem.

        It defines:

            :attributes: None.
            :methods:
                | create - Creates TelemetryListenerProvides from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls, dependencies: TelemetryListenerDependencies
    ) -> TelemetryListenerProvides:
        '''
            Creates TelemetryListenerProvides from TelemetryListenerDependencies.

            :param dependencies: Collaborator bundle for telemetry listener.
            :return: Assembled TelemetryListenerProvides bundle.
            :exceptions: None.
        '''
        decoder = TelemetryDecoder(
            codec=dependencies.codec,
            inspector=dependencies.inspector,
            sink=dependencies.sink,
            clock=dependencies.clock,
        )
        loop = TelemetryListenerLoop(
            receiver=dependencies.receiver,
            decoder=decoder,
            stop_flag=dependencies.stop_flag,
            timeout_sec=dependencies.timeout_sec,
        )
        listener = TelemetryListener(
            loop=loop,
            decoder=decoder,
            controller=dependencies.controller,
        )
        return TelemetryListenerProvides(listener=listener)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
