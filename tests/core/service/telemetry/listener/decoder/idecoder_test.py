# -*- coding: UTF-8 -*-

'''
Module
    idecoder_test.py
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
    Unit tests for ITelemetryDecoder structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.codec.icodec import IBinaryCodec
from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector
from botracked.core.service.telemetry.listener.decoder.decoder import TelemetryDecoder
from botracked.core.service.telemetry.listener.decoder.idecoder import ITelemetryDecoder
from botracked.core.service.telemetry.protocol.isink import ITelemetrySink

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryDecoderProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of ITelemetryDecoder.
    '''

    def test_decoder_protocol_conformance(self) -> None:
        '''
            Verifies TelemetryDecoder satisfies ITelemetryDecoder structurally.

            :exceptions: None.
        '''
        clock = Mock(spec=IClock)
        clock.monotonic.return_value = 0.0
        decoder = TelemetryDecoder(
            codec=Mock(spec=IBinaryCodec),
            inspector=Mock(spec=ITelemetryInspector),
            sink=Mock(spec=ITelemetrySink),
            clock=clock,
        )
        self.assertIsInstance(decoder, ITelemetryDecoder)
        self.assertNotIsInstance(object(), ITelemetryDecoder)


if __name__ == '__main__':
    main()
