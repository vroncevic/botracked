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
    Unit tests for TelemetryObserverDependencies.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.infrastructure.gui.telemetry.iview import ITelemetryView
from botracked.infrastructure.gui.telemetry.observer.dependencies import TelemetryObserverDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryObserverDependenciesTest(TestCase):
    '''
        Tests TelemetryObserverDependencies field retention.
    '''

    def test_fields(self) -> None:
        '''
            Verifies scheduler, view, and packet_sink fields.

            :exceptions: None.
        '''
        sched = MagicMock(spec=Tk)
        view = MagicMock(spec=ITelemetryView)
        sink = MagicMock(spec=IPacketStreamSink)
        deps = TelemetryObserverDependencies(
            scheduler=sched,
            view=view,
            packet_sink=sink,
        )
        self.assertIs(deps.scheduler, sched)
        self.assertIs(deps.view, view)
        self.assertIs(deps.packet_sink, sink)

if __name__ == '__main__':
    main()
