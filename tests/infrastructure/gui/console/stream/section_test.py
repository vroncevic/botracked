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
    Unit tests for ConsoleStreamSection.
'''

from __future__ import annotations

from tkinter import TclError
from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.console.stream.section import ConsoleStreamSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class ConsoleStreamSectionTest(TestCase):
    '''
        Tests ConsoleStreamSection packet trace, log entries, clear, and copy.
    '''

    @patch('botracked.infrastructure.gui.console.stream.section.Frame')
    @patch('botracked.infrastructure.gui.console.stream.section.Text')
    @patch('botracked.infrastructure.gui.console.stream.section.Scrollbar')
    def test_stream_methods(
        self,
        _mock_scroll: MagicMock,
        mock_text_cls: MagicMock,
        mock_frame_cls: MagicMock,
    ) -> None:
        '''
            Verifies write_entry, append_packet, clear, and copy_selection.

            :param _mock_scroll: Patched Scrollbar constructor.
            :param mock_text_cls: Patched Text constructor.
            :param mock_frame_cls: Patched Frame constructor.
            :exceptions: None.
        '''
        txt = MagicMock()
        txt.get.side_effect = [TclError('no sel'), 'all text']
        mock_text_cls.return_value = txt

        sec = ConsoleStreamSection(parent=MagicMock(spec=Frame))
        self.assertEqual(ConsoleStreamSection.STREAM_HEIGHT, 16)
        self.assertEqual(mock_text_cls.call_args.kwargs['height'], 16)
        self.assertIsNotNone(sec.get_widget())
        sec.write_entry('INFO', 'ready')
        sec.append_packet('TX', 'CMD_PING', 'AA 01')
        sec.clear()
        sec.copy_selection()
        mock_frame_cls.return_value.clipboard_append.assert_called_once_with('all text')


if __name__ == '__main__':
    main()
