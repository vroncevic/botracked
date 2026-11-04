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
    Unit tests for CockpitFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.bundle.services import BotServicesBundle
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.infrastructure.gui.console.observer.isink import IPacketStreamSink
from botracked.setup.gui.cockpit.dependencies import CockpitDependencies
from botracked.setup.gui.cockpit.factory import CockpitFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CockpitFactoryTest(TestCase):
    '''
        Tests CockpitFactory headless assembly with mocked widgets.
    '''

    @patch('botracked.infrastructure.gui.motion.panel.Label')
    @patch('botracked.setup.gui.cockpit.factory.Frame')
    @patch('botracked.infrastructure.gui.motion.dpad.section.Frame')
    @patch('botracked.infrastructure.gui.motion.dpad.section.Button')
    @patch('botracked.infrastructure.gui.motion.speed.section.Frame')
    @patch('botracked.infrastructure.gui.motion.speed.section.Label')
    @patch('botracked.infrastructure.gui.motion.speed.section.Scale')
    @patch('botracked.infrastructure.gui.motion.speed.section.DoubleVar')
    @patch('botracked.infrastructure.gui.motion.speed.section.StringVar')
    @patch('botracked.infrastructure.gui.telemetry.card.section.Frame')
    @patch('botracked.infrastructure.gui.telemetry.card.section.Label')
    @patch('botracked.infrastructure.gui.telemetry.card.section.StringVar')
    @patch('botracked.infrastructure.gui.telemetry.panel.Frame')
    @patch('botracked.infrastructure.gui.telemetry.panel.Label')
    @patch('botracked.infrastructure.gui.telemetry.panel.StringVar')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies CockpitFactory wires motion, telemetry, observer.

            :param _mocks: Patched Tkinter widget constructors.
            :exceptions: None.
        '''
        srv = MagicMock(spec=BotServicesBundle)
        srv.motion = MagicMock()
        srv.telemetry = MagicMock()
        root = MagicMock(spec=Tk)

        prov = CockpitFactory.create(
            CockpitDependencies(
                root=root,
                parent=root,
                services=srv,
                log_listener=MagicMock(spec=ILogListener),
                packet_sink=MagicMock(spec=IPacketStreamSink),
            )
        )
        srv.telemetry.add_observer.assert_called_once()
        root.bind.assert_called_once()
        self.assertIsNotNone(prov.motion_panel)
        self.assertEqual(CockpitFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
