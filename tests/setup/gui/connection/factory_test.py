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
    Unit tests for ConnectionFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.connection_preference import ConnectionPreference
from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.core.service.bundle.runners import BotRunnersBundle
from botracked.core.service.connection.iservice import IBotConnectionService
from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.infrastructure.gui.connection.ipanel import IConnectionPanel
from botracked.infrastructure.gui.console.observer.ilistener import ILogListener
from botracked.setup.gui.connection.dependencies import ConnectionDependencies
from botracked.setup.gui.connection.factory import ConnectionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionFactoryTest(TestCase):
    '''
        Tests ConnectionFactory headless assembly with mocked widgets.
    '''

    @patch('botracked.setup.gui.connection.factory.Frame')
    @patch('botracked.infrastructure.gui.connection.serial.section.Frame')
    @patch('botracked.infrastructure.gui.connection.serial.section.Label')
    @patch('botracked.infrastructure.gui.connection.serial.section.Combobox')
    @patch('botracked.infrastructure.gui.connection.serial.section.Button')
    @patch('botracked.infrastructure.gui.connection.serial.section.StringVar')
    @patch('botracked.infrastructure.gui.connection.status.section.Frame')
    @patch('botracked.infrastructure.gui.connection.status.section.Label')
    @patch('botracked.infrastructure.gui.connection.status.section.Button')
    @patch('botracked.infrastructure.gui.connection.status.section.StringVar')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies ConnectionFactory wires IConnectionPanel cleanly.

            :param _mocks: Patched Tkinter widget constructors.
            :exceptions: None.
        '''
        prefs = MagicMock(spec=IConnectionPreferencesRepository)
        prefs.has_preference.return_value = True
        prefs.load_preference.return_value = ConnectionPreference(
            port='/dev/ttyUSB0', baud=57600
        )
        scanner = MagicMock(spec=IPortScanner)
        scanner.scan_ports.return_value = ('/dev/ttyUSB0',)
        runners = MagicMock(spec=BotRunnersBundle)
        runners.listener = MagicMock()
        runners.poller = MagicMock()
        runners.mission = MagicMock()

        panel = ConnectionFactory.create(
            ConnectionDependencies(
                root=MagicMock(spec=Tk),
                connection_service=MagicMock(spec=IBotConnectionService),
                runners=runners,
                preferences_repository=prefs,
                port_scanner=scanner,
                log_listener=MagicMock(spec=ILogListener),
            )
        )
        self.assertIsInstance(panel, IConnectionPanel)
        self.assertEqual(ConnectionFactory.get_version(), '1.0.2')

        prefs.load_preference.side_effect = PreferencesError('failed')
        panel2 = ConnectionFactory.create(
            ConnectionDependencies(
                root=MagicMock(spec=Tk),
                connection_service=MagicMock(spec=IBotConnectionService),
                runners=runners,
                preferences_repository=prefs,
                port_scanner=scanner,
                log_listener=MagicMock(spec=ILogListener),
            )
        )
        self.assertIsInstance(panel2, IConnectionPanel)


if __name__ == '__main__':
    main()
