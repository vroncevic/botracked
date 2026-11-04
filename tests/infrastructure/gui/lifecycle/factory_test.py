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
    Unit tests for GuiLifecycleFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.motion.runner.irunner import IMissionRunner
from botracked.core.service.telemetry.listener.ilistener import ITelemetryListener
from botracked.core.service.telemetry.poller.ipoller import ITelemetryPoller
from botracked.infrastructure.gui.lifecycle.dependencies import GuiLifecycleDependencies
from botracked.infrastructure.gui.lifecycle.factory import GuiLifecycleFactory
from botracked.infrastructure.gui.lifecycle.irunner import IGuiLifecycleRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiLifecycleFactoryTest(TestCase):
    '''
        Tests GuiLifecycleFactory wiring and version.
    '''

    def test_create_and_version(self) -> None:
        '''
            Verifies GuiLifecycleFactory creates runner.

            :exceptions: None.
        '''
        prov = GuiLifecycleFactory.create(
            GuiLifecycleDependencies(
                root=MagicMock(spec=Tk),
                connection_service=MagicMock(spec=IBotConnectionService),
                listener=MagicMock(spec=ITelemetryListener),
                poller=MagicMock(spec=ITelemetryPoller),
                mission_runner=MagicMock(spec=IMissionRunner),
            )
        )
        self.assertIsInstance(prov.runner, IGuiLifecycleRunner)
        self.assertEqual(GuiLifecycleFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
