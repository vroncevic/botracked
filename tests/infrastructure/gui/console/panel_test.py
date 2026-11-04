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
    Unit tests for ConsolePanel.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.console.panel import ConsolePanel
from botracked.infrastructure.gui.console.stream.isection import IConsoleStreamSection
from botracked.infrastructure.gui.console.toolbar.isection import IConsoleToolbarSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsolePanelTest(TestCase):
    '''
        Tests ConsolePanel delegation to injected stream and toolbar sections.
    '''

    def test_console_panel_delegation(self) -> None:
        '''
            Verifies write_entry, append_packet, clear, and copy_selection.

            :exceptions: None.
        '''
        stream = MagicMock(spec=IConsoleStreamSection)
        toolbar = MagicMock(spec=IConsoleToolbarSection)
        panel = ConsolePanel(
            frame=MagicMock(spec=Frame),
            stream_section=stream,
            toolbar_section=toolbar,
        )
        self.assertIsNotNone(panel.get_widget())
        panel.write_entry('INFO', 'ok')
        stream.write_entry.assert_called_once_with('INFO', 'ok')
        panel.append_packet('RX', 'STATUS', 'AA 09')
        stream.append_packet.assert_called_once_with('RX', 'STATUS', 'AA 09')
        panel.clear()
        stream.clear.assert_called_once()
        panel.copy_selection()
        stream.copy_selection.assert_called_once()


if __name__ == '__main__':
    main()
