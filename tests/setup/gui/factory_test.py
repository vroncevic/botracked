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
    Unit tests for BotGuiSessionFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.core.service.bundle.services import BotServicesBundle
from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.connection.ipanel import IConnectionPanel
from botracked.infrastructure.gui.mission.ipanel import IMissionPanel
from botracked.infrastructure.gui.motion.ipanel import IMotionPanel
from botracked.infrastructure.gui.session.isession import IGuiSession
from botracked.infrastructure.gui.telemetry.ipanel import ITelemetryPanel
from botracked.setup.gui.cockpit.provides import CockpitProvides
from botracked.setup.gui.dependencies import BotGuiSessionDependencies
from botracked.setup.gui.factory import BotGuiSessionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BotGuiSessionFactoryTest(TestCase):
    '''
        Tests BotGuiSessionFactory headless session composition.
    '''

    @patch('botracked.setup.gui.factory.Tk')
    @patch('botracked.setup.gui.factory.Style')
    @patch('botracked.setup.gui.factory.Frame')
    @patch('botracked.infrastructure.gui.layout.builder.Frame')
    @patch('botracked.infrastructure.gui.console.stream.section.Frame')
    @patch('botracked.infrastructure.gui.console.stream.section.Text')
    @patch('botracked.infrastructure.gui.console.stream.section.Scrollbar')
    @patch('botracked.infrastructure.gui.console.toolbar.section.Frame')
    @patch('botracked.infrastructure.gui.console.toolbar.section.Label')
    @patch('botracked.infrastructure.gui.console.toolbar.section.Button')
    @patch('botracked.setup.gui.factory.ConnectionFactory.create')
    @patch('botracked.setup.gui.factory.MissionFactory.create')
    @patch('botracked.setup.gui.factory.CockpitFactory.create')
    def test_create_and_version(
        self,
        mock_cockpit: MagicMock,
        mock_mission: MagicMock,
        mock_conn: MagicMock,
        *_tk_mocks: MagicMock,
    ) -> None:
        '''
            Verifies BotGuiSessionFactory mounts all panels and returns session.

            :param mock_cockpit: Mocked cockpit sub-factory.
            :param mock_mission: Mocked mission sub-factory.
            :param mock_conn: Mocked connection sub-factory.
            :param _tk_mocks: Patched Tkinter constructors.
            :exceptions: None.
        '''
        mock_conn.return_value = MagicMock(spec=IConnectionPanel)
        mock_mission.return_value = MagicMock(spec=IMissionPanel)
        mock_cockpit.return_value = CockpitProvides(
            motion_panel=MagicMock(spec=IMotionPanel),
            telemetry_panel=MagicMock(spec=ITelemetryPanel),
        )
        services = MagicMock(spec=BotServicesBundle)
        services.connection = MagicMock()
        services.dsl = MagicMock()
        runners = MagicMock(spec=BotRunnersBundle)
        runners.listener = MagicMock()
        runners.poller = MagicMock()
        runners.mission = MagicMock()
        runtime = BotRuntimeBundle(services=services, runners=runners)

        session = BotGuiSessionFactory.create(
            BotGuiSessionDependencies(
                runtime=runtime,
                preferences_repository=MagicMock(
                    spec=IConnectionPreferencesRepository
                ),
                port_scanner=MagicMock(spec=IPortScanner),
                preset_repository=MagicMock(spec=IMissionPresetRepository),
            )
        )
        self.assertIsInstance(session, IGuiSession)
        self.assertEqual(BotGuiSessionFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
