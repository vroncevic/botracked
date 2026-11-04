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
    Unit tests for ConnectionStatusSection.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.connection.status.ilistener import IConnectionControlListener
from botracked.infrastructure.gui.connection.status.section import ConnectionStatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConnectionStatusSectionTest(TestCase):
    '''
        Tests ConnectionStatusSection badge and button toggle state.
    '''

    @patch('botracked.infrastructure.gui.connection.status.section.Frame')
    @patch('botracked.infrastructure.gui.connection.status.section.Label')
    @patch('botracked.infrastructure.gui.connection.status.section.Button')
    @patch('botracked.infrastructure.gui.connection.status.section.StringVar')
    def test_status_section_methods(self, *_mocks: MagicMock) -> None:
        '''
            Verifies bind_listener, set_state, and is_connected.

            :param _mocks: Patched Tkinter constructors.
            :exceptions: None.
        '''
        sec = ConnectionStatusSection(parent=MagicMock(spec=Frame))
        self.assertFalse(sec.is_connected())
        self.assertIsNotNone(sec.get_widget())

        lst = MagicMock(spec=IConnectionControlListener)
        sec.bind_listener(lst)
        sec.set_state(True, 'Online')
        self.assertTrue(sec.is_connected())


if __name__ == '__main__':
    main()
