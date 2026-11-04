# -*- coding: UTF-8 -*-

'''
Module
    iidentifier_test.py
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
    Unit tests for IIdentifierScanner protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import Mock

from botracked.core.service.dsl.lexer.identifier.identifier import IdentifierScanner
from botracked.core.service.dsl.lexer.identifier.iidentifier import IIdentifierScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IdentifierScannerProtocolTest(TestCase):
    '''
        Verifies runtime structural subtyping of IIdentifierScanner.
    '''

    def test_conformance(self) -> None:
        '''
            Verifies IdentifierScanner and Mock satisfy IIdentifierScanner.

            :exceptions: None.
        '''
        self.assertIsInstance(IdentifierScanner(), IIdentifierScanner)
        self.assertIsInstance(Mock(spec=IIdentifierScanner), IIdentifierScanner)
        self.assertNotIsInstance(object(), IIdentifierScanner)


if __name__ == '__main__':
    main()
