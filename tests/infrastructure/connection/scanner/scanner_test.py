# -*- coding: UTF-8 -*-

'''
Module
    scanner_test.py
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
    Unit tests for PortScanner adapter querying system hardware communication ports.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.service.connection.scanner.iscanner import IPortScanner
from botracked.infrastructure.connection.scanner.scanner import PortScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScannerTest(TestCase):
    '''
        Tests PortScanner device discovery, availability check, and str().
    '''

    _scanner: PortScanner

    def setUp(self) -> None:
        '''
            Sets up test fixture before each test execution.

            :exceptions: None.
        '''
        self._scanner = PortScanner(include_links=True)

    def test_protocol_and_str(self) -> None:
        '''
            Verifies PortScanner conforms to IPortScanner and formats str().

            :exceptions: None.
        '''
        self.assertIsInstance(self._scanner, IPortScanner)
        self.assertIn('PortScanner', str(self._scanner))
        self.assertIsInstance(self._scanner.get_version(), str)
        self.assertTrue(len(self._scanner.get_version()) > 0)

    @patch('botracked.infrastructure.connection.scanner.scanner.comports')
    def test_scan_ports(self, mock_comports: MagicMock) -> None:
        '''
            Verifies scan_ports passes include_links to comports.

            :param mock_comports: Mock of serial.tools.list_ports.comports.
            :exceptions: None.
        '''
        port1 = MagicMock()
        port1.device = '/dev/ttyUSB0'
        port2 = MagicMock()
        port2.device = '/dev/ttyUSB1'
        mock_comports.return_value = [port1, port2]

        self.assertEqual(
            self._scanner.scan_ports(), ['/dev/ttyUSB0', '/dev/ttyUSB1']
        )
        mock_comports.assert_called_with(include_links=True)


if __name__ == '__main__':
    main()
