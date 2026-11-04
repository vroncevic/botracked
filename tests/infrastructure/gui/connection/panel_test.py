# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
    Unit tests for ConnectionPanel.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.core.model.exceptions.preferences_error import PreferencesError
from botracked.core.service.connection.preferences.irepository import IConnectionPreferencesRepository
from botracked.infrastructure.gui.connection.dependencies import ConnectionPanelDependencies
from botracked.infrastructure.gui.connection.idelegate import IConnectionActionDelegate
from botracked.infrastructure.gui.connection.panel import ConnectionPanel
from botracked.infrastructure.gui.connection.serial.isection import ISerialSection
from botracked.infrastructure.gui.connection.status.isection import IConnectionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConnectionPanelTest(TestCase):
    '''
        Tests ConnectionPanel connect/disconnect toggle and port refresh.
    '''

    def test_toggle_connection_and_refresh(self) -> None:
        '''
            Verifies connect saves preference and disconnect resets badge.

            :exceptions: None.
        '''
        dlg = MagicMock(spec=IConnectionActionDelegate)
        dlg.handle_connect.return_value = (True, 'Connected')
        prefs = MagicMock(spec=IConnectionPreferencesRepository)
        serial_sec = MagicMock(spec=ISerialSection)
        serial_sec.get_port.return_value = '/dev/ttyACM0'
        serial_sec.get_baud.return_value = 115200
        status_sec = MagicMock(spec=IConnectionStatusSection)
        status_sec.is_connected.return_value = False

        panel = ConnectionPanel(
            ConnectionPanelDependencies(
                frame=MagicMock(spec=Frame),
                delegate=dlg,
                preferences_repo=prefs,
                serial_section=serial_sec,
                status_section=status_sec,
            )
        )
        self.assertIsNotNone(panel.get_widget())
        panel.on_toggle_connection()
        prefs.save_preference.assert_called_once()
        status_sec.set_state.assert_called_with(True, 'Connected')

        prefs.save_preference.side_effect = PreferencesError('save failed')
        panel.on_toggle_connection()
        prefs.save_preference.side_effect = None

        status_sec.is_connected.return_value = True
        panel.on_toggle_connection()
        dlg.handle_disconnect.assert_called_once()

        panel.on_refresh_ports()
        serial_sec.refresh_ports.assert_called_once()


if __name__ == '__main__':
    main()
