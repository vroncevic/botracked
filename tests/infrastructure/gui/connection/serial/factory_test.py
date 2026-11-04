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
    Unit tests for SerialSectionFactory.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.connection.iport_delegate import IPortRefreshDelegate
from botracked.infrastructure.gui.connection.serial.dependencies import SerialSectionDependencies
from botracked.infrastructure.gui.connection.serial.factory import SerialSectionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class SerialSectionFactoryTest(TestCase):
    '''
        Tests SerialSectionFactory wiring and version.
    '''

    @patch('botracked.infrastructure.gui.connection.serial.section.Frame')
    @patch('botracked.infrastructure.gui.connection.serial.section.Label')
    @patch('botracked.infrastructure.gui.connection.serial.section.Combobox')
    @patch('botracked.infrastructure.gui.connection.serial.section.Button')
    @patch('botracked.infrastructure.gui.connection.serial.section.StringVar')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies SerialSectionFactory creates ISerialSection.

            :param _mocks: Patched Tkinter widget constructors.
            :exceptions: None.
        '''
        prov = SerialSectionFactory.create(
            SerialSectionDependencies(
                parent=MagicMock(spec=Frame),
                delegate=MagicMock(spec=IPortRefreshDelegate),
                default_port='/dev/ttyACM0',
                default_baud=115200,
            )
        )
        self.assertIsNotNone(prov.section)
        self.assertEqual(SerialSectionFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
