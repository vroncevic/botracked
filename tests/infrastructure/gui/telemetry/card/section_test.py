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
    Unit tests for TelemetryCardSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.core.model.motion_command import MotionCommand
from botracked.core.model.system_mode import SystemMode
from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.telemetry.card.isection import ITelemetryCardSection
from botracked.infrastructure.gui.telemetry.card.section import TelemetryCardSection
from botracked.infrastructure.gui.telemetry.config import TelemetryPanelConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryCardSectionTest(TestCase):
    '''
        Tests TelemetryCardSection metric updates across operating modes.
    '''

    @patch('botracked.infrastructure.gui.telemetry.card.section.Label')
    @patch('botracked.infrastructure.gui.telemetry.card.section.StringVar')
    @patch('botracked.infrastructure.gui.telemetry.card.section.Frame')
    def test_update_and_reset_metrics(self, *_mocks: MagicMock) -> None:
        '''
            Verifies update_metrics across NORMAL, DEGRADED, PANIC and reset.

            :param _mocks: Patched Tkinter widget and variable classes.
            :exceptions: None.
        '''
        frame_cls, svar_cls, _lbl_cls = _mocks
        mode_var = MagicMock()
        mode_var.get.return_value = 'NORMAL'
        svar_cls.side_effect = [
            mode_var,
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        sec = TelemetryCardSection(MagicMock(spec=Frame), TelemetryPanelConfig())
        self.assertIsInstance(sec, ITelemetryCardSection)
        self.assertIsNotNone(sec.get_widget())
        self.assertIsNotNone(frame_cls.return_value)

        for sys_mode in (SystemMode.NORMAL, SystemMode.DEGRADED, SystemMode.PANIC):
            snap = TelemetryData(
                system_mode=str(sys_mode),
                motion=MotionCommand.TURN_LEFT,
                speed_pwm=160,
                error_code=2,
                uptime_ms=2500,
                left_motor_state='FWD',
                right_motor_state='REV',
                last_updated=1.0,
                is_connected=True,
            )
            sec.update_metrics(snap)

        self.assertEqual(sec.get_mode_text(), 'NORMAL')
        sec.reset_metrics()
        mode_var.set.assert_called_with('OFFLINE')


if __name__ == '__main__':
    main()
