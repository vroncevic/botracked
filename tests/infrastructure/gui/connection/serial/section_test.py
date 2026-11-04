# -*- coding: UTF-8 -*-

'''
Module
    section_test.py
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
    Unit tests for SerialSection.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.connection.iport_delegate import IPortRefreshDelegate
from botracked.infrastructure.gui.connection.serial.section import SerialSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class SerialSectionTest(TestCase):
    '''
        Tests SerialSection headless port/baud reading, refresh, and state.
    '''

    @patch('botracked.infrastructure.gui.connection.serial.section.Frame')
    @patch('botracked.infrastructure.gui.connection.serial.section.Label')
    @patch('botracked.infrastructure.gui.connection.serial.section.Combobox')
    @patch('botracked.infrastructure.gui.connection.serial.section.Button')
    @patch('botracked.infrastructure.gui.connection.serial.section.StringVar')
    def test_serial_section_operations(
        self, mock_svar: MagicMock, *_mocks: MagicMock
    ) -> None:
        '''
            Verifies port/baud getters, refresh_ports, and set_enabled.

            :param mock_svar: Patched StringVar constructor.
            :param _mocks: Patched ttk constructors.
            :exceptions: None.
        '''
        port_var = MagicMock()
        port_var.get.return_value = ''
        baud_var = MagicMock()
        baud_var.get.return_value = '115200'
        mock_svar.side_effect = [port_var, baud_var]

        dlg = MagicMock(spec=IPortRefreshDelegate)
        dlg.handle_refresh_ports.return_value = ('/dev/ttyACM0',)
        sec = SerialSection(
            parent=MagicMock(spec=Frame),
            delegate=dlg,
            default_port='',
            default_baud=115200,
        )
        self.assertIsNotNone(sec.get_widget())
        self.assertEqual(sec.get_port(), '')
        self.assertEqual(sec.get_baud(), 115200)
        baud_var.get.return_value = 'bad'
        self.assertEqual(sec.get_baud(), 9600)

        sec.refresh_ports()
        port_var.set.assert_called_with('/dev/ttyACM0')
        sec.set_enabled(False)
        sec.set_enabled(True)


if __name__ == '__main__':
    main()
