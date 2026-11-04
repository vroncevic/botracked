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
    Unit tests for ConsoleToolbarSection.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.console.stream.isection import IConsoleStreamSection
from botracked.infrastructure.gui.console.toolbar.section import ConsoleToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsoleToolbarSectionTest(TestCase):
    '''
        Tests ConsoleToolbarSection clear and copy actions.
    '''

    @patch('botracked.infrastructure.gui.console.toolbar.section.Frame')
    @patch('botracked.infrastructure.gui.console.toolbar.section.Label')
    @patch('botracked.infrastructure.gui.console.toolbar.section.Button')
    def test_clear_and_copy(self, *_mocks: MagicMock) -> None:
        '''
            Verifies on_clear and on_copy forward to stream_section.

            :param _mocks: Patched Tkinter constructors.
            :exceptions: None.
        '''
        stream = MagicMock(spec=IConsoleStreamSection)
        sec = ConsoleToolbarSection(
            parent=MagicMock(spec=Frame), stream_section=stream
        )
        self.assertIsNotNone(sec.get_widget())
        sec.on_clear()
        stream.clear.assert_called_once()
        sec.on_copy()
        stream.copy_selection.assert_called_once()


if __name__ == '__main__':
    main()
