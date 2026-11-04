# -*- coding: UTF-8 -*-

'''
Module
    launcher_test.py
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
    Unit tests for GuiSessionLauncher.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.bundle.runtime import BotRuntimeBundle
from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.core.service.dsl.preset.irepository import IMissionPresetRepository
from botracked.infrastructure.gui.igui import IGUI
from botracked.infrastructure.gui.session.isession import IGuiSession
from botracked.setup.gui.dependencies import BotGuiSessionDependencies
from botracked.setup.gui.launcher import GuiSessionLauncher

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiSessionLauncherTest(TestCase):
    '''
        Tests GuiSessionLauncher lazy session creation and shutdown.
    '''

    @patch('botracked.setup.gui.launcher.BotGuiSessionFactory.create')
    def test_launch_set_script_and_shutdown(
        self, mock_create: MagicMock
    ) -> None:
        '''
            Verifies launch, script forwarding, shutdown, and __str__.

            :param mock_create: Mocked BotGuiSessionFactory.create.
            :exceptions: None.
        '''
        session = MagicMock(spec=IGuiSession)
        mock_create.return_value = session
        deps = BotGuiSessionDependencies(
            runtime=MagicMock(spec=BotRuntimeBundle),
            preferences_repository=MagicMock(
                spec=IConnectionPreferencesRepository
            ),
            port_scanner=MagicMock(spec=IPortScanner),
            preset_repository=MagicMock(spec=IMissionPresetRepository),
        )
        launcher = GuiSessionLauncher(deps)
        self.assertIsInstance(launcher, IGUI)
        self.assertTrue(launcher.is_initialized())
        self.assertTrue(str(launcher))

        launcher.load_script('PING\n')
        launcher.start()
        session.set_script.assert_called_once_with('PING\n')
        session.start.assert_called_once()

        launcher.load_script('STOP\n')
        session.set_script.assert_called_with('STOP\n')

        launcher.stop()
        session.stop.assert_called_once()


if __name__ == '__main__':
    main()
