# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for TelemetryObserverFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.telemetry.protocol.iobserver import ITelemetryObserver
from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.infrastructure.gui.telemetry.iview import ITelemetryView
from botracked.infrastructure.gui.telemetry.observer.dependencies import TelemetryObserverDependencies
from botracked.infrastructure.gui.telemetry.observer.factory import TelemetryObserverFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryObserverFactoryTest(TestCase):
    '''
        Tests TelemetryObserverFactory assembly and version string.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies create produces observer port and version 1.0.2.

            :exceptions: None.
        '''
        deps = TelemetryObserverDependencies(
            scheduler=MagicMock(spec=Tk),
            view=MagicMock(spec=ITelemetryView),
            packet_sink=MagicMock(spec=IPacketStreamSink),
        )
        provides = TelemetryObserverFactory.create(deps)
        self.assertIsInstance(provides.observer, ITelemetryObserver)
        self.assertEqual(TelemetryObserverFactory.get_version(), '1.0.2')

if __name__ == '__main__':
    main()
