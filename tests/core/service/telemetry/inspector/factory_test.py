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
    Unit tests for TelemetryInspectorFactory subsystem assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.concurrency.iclock import IClock
from botracked.core.service.telemetry.inspector.dependencies import TelemetryInspectorDependencies
from botracked.core.service.telemetry.inspector.factory import TelemetryInspectorFactory
from botracked.core.service.telemetry.inspector.iinspector import ITelemetryInspector

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryInspectorFactoryTest(TestCase):
    '''
        Verifies TelemetryInspectorFactory assembly and version reporting.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies TelemetryInspectorFactory builds ITelemetryInspector port.

            :exceptions: None.
        '''
        prov = TelemetryInspectorFactory.create(
            TelemetryInspectorDependencies(clock=Mock(spec=IClock))
        )
        self.assertIsInstance(prov.inspector, ITelemetryInspector)
        self.assertEqual(TelemetryInspectorFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
