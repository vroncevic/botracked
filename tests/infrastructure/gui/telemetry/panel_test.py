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
    Unit tests for TelemetryPanel composite component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.telemetry.card.isection import ITelemetryCardSection
from botracked.infrastructure.gui.telemetry.config import TelemetryPanelConfig
from botracked.infrastructure.gui.telemetry.ipanel import ITelemetryPanel
from botracked.infrastructure.gui.telemetry.iview import ITelemetryView
from botracked.infrastructure.gui.telemetry.panel import TelemetryPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryPanelTest(TestCase):
    '''
        Tests TelemetryPanel delegation and packet counter updates.
    '''

    @patch('botracked.infrastructure.gui.telemetry.panel.Label')
    @patch('botracked.infrastructure.gui.telemetry.panel.Frame')
    @patch('botracked.infrastructure.gui.telemetry.panel.StringVar')
    def test_panel_methods(
        self, svar_cls: MagicMock, _frm_cls: MagicMock, _lbl_cls: MagicMock
    ) -> None:
        '''
            Verifies telemetry forwarding, packet count, and reset_telemetry.

            :param svar_cls: Patched StringVar class.
            :param _frm_cls: Patched Frame class.
            :param _lbl_cls: Patched Label class.
            :exceptions: None.
        '''
        pkt_var = MagicMock()
        svar_cls.return_value = pkt_var
        root_frame = MagicMock(spec=Frame)
        cards = MagicMock(spec=ITelemetryCardSection)
        panel = TelemetryPanel(root_frame, cards, TelemetryPanelConfig())
        self.assertIsInstance(panel, ITelemetryPanel)
        self.assertIsInstance(panel, ITelemetryView)
        self.assertIs(panel.get_widget(), root_frame)

        sample = TelemetryData('NORMAL', MotionCommand.FORWARD, 200, 0, 500, 'FWD', 'FWD', 1.0, True)
        panel.update_telemetry(sample)
        cards.update_metrics.assert_called_once_with(sample)

        panel.update_packet_count(7)
        pkt_var.set.assert_called_with('Pkts: 7')

        panel.reset_telemetry()
        cards.reset_metrics.assert_called_once()
        pkt_var.set.assert_called_with('Pkts: 0')


if __name__ == '__main__':
    main()
