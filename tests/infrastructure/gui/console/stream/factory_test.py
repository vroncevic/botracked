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
    Unit tests for ConsoleStreamFactory.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.console.stream.dependencies import ConsoleStreamDependencies
from botracked.infrastructure.gui.console.stream.factory import ConsoleStreamFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsoleStreamFactoryTest(TestCase):
    '''
        Tests ConsoleStreamFactory wiring and version.
    '''

    @patch('botracked.infrastructure.gui.console.stream.section.Frame')
    @patch('botracked.infrastructure.gui.console.stream.section.Text')
    @patch('botracked.infrastructure.gui.console.stream.section.Scrollbar')
    def test_create_and_version(self, *_mocks: MagicMock) -> None:
        '''
            Verifies ConsoleStreamFactory creates IConsoleStreamSection.

            :param _mocks: Patched Tkinter constructors.
            :exceptions: None.
        '''
        prov = ConsoleStreamFactory.create(
            ConsoleStreamDependencies(parent=MagicMock(spec=Frame))
        )
        self.assertIsNotNone(prov.section)
        self.assertEqual(ConsoleStreamFactory.get_version(), '1.0.2')


if __name__ == '__main__':
    main()
