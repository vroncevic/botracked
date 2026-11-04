# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for FrameDispatcherDependencies immutable bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.connection.dispatcher.dependencies import FrameDispatcherDependencies
from botracked.core.service.connection.port.istatus import IConnectionStatus
from botracked.core.service.connection.transmitter.protocol.itransmitter import IByteTransmitter
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDispatcherDependenciesTest(TestCase):
    '''
        Verifies FrameDispatcherDependencies fields and immutability.
    '''

    def test_fields_and_frozen(self) -> None:
        '''
            Verifies codec, transmitter, status, and sink storage and frozen.

            :exceptions: None.
        '''
        codec = Mock(spec=IBinaryCodec)
        tx = Mock(spec=IByteTransmitter)
        status = Mock(spec=IConnectionStatus)
        sink = Mock(spec=ITelemetrySink)
        deps = FrameDispatcherDependencies(
            codec=codec, transmitter=tx, status=status, sink=sink
        )
        self.assertIs(deps.codec, codec)
        self.assertIs(deps.transmitter, tx)
        self.assertIs(deps.status, status)
        self.assertIs(deps.sink, sink)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'codec', codec)


if __name__ == '__main__':
    main()
