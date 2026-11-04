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
    Unit tests for LayoutFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.layout.dependencies import LayoutDependencies
from botracked.infrastructure.gui.layout.factory import LayoutFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class LayoutFactoryTest(TestCase):
    '''
        Tests LayoutFactory wiring and version.
    '''

    @patch('botracked.infrastructure.gui.layout.builder.Frame')
    def test_create_and_version(self, mock_frame: MagicMock) -> None:
        '''
            Verifies LayoutFactory creates valid ILayoutBuilder and LayoutSlots.

            :param mock_frame: Patched ttk Frame constructor.
            :exceptions: None.
        '''
        root = MagicMock(spec=Tk)
        prov = LayoutFactory.create(LayoutDependencies(root=root))
        self.assertIs(prov.builder.get_root(), root)
        self.assertTrue(mock_frame.called)
        self.assertEqual(LayoutFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
