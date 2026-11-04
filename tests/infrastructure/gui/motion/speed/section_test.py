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
    Unit tests for MotionSpeedSection leaf UI component.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate
from botracked.infrastructure.gui.motion.speed.isection import IMotionSpeedSection
from botracked.infrastructure.gui.motion.speed.section import MotionSpeedSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionSpeedSectionTest(TestCase):
    '''
        Tests MotionSpeedSection PWM clamping, slider callback, and state.
    '''

    @patch('botracked.infrastructure.gui.motion.speed.section.Scale')
    @patch('botracked.infrastructure.gui.motion.speed.section.Label')
    @patch('botracked.infrastructure.gui.motion.speed.section.StringVar')
    @patch('botracked.infrastructure.gui.motion.speed.section.DoubleVar')
    @patch('botracked.infrastructure.gui.motion.speed.section.Frame')
    def test_speed_operations(self, *_mocks: MagicMock) -> None:
        '''
            Verifies get_speed, set_speed, on_slider_change, and set_enabled.

            :param _mocks: Patched Tkinter widget and variable classes.
            :exceptions: None.
        '''
        frame_cls, dvar_cls, _svar_cls, _lbl_cls, scale_cls = _mocks
        dvar = MagicMock()
        dvar.get.return_value = 180.0
        dvar_cls.return_value = dvar
        scale_inst = MagicMock()
        scale_cls.return_value = scale_inst
        delegate = MagicMock(spec=IMotionActionDelegate)

        sec = MotionSpeedSection(MagicMock(spec=Frame), delegate, 180)
        self.assertIsInstance(sec, IMotionSpeedSection)
        self.assertIs(sec.get_widget(), frame_cls.return_value)
        self.assertEqual(sec.get_speed(), 180)

        sec.set_speed(300)
        dvar.set.assert_called_with(255.0)

        sec.on_slider_change('200.4')
        delegate.handle_speed.assert_called_with(200)

        sec.on_slider_change('not-a-float')
        delegate.handle_speed.assert_called_with(150)

        sec.set_enabled(False)
        scale_inst.configure.assert_called_with(state='disabled')


if __name__ == '__main__':
    main()
