# -*- coding: UTF-8 -*-

'''
Module
    slots_test.py
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
    Unit tests for LayoutSlots container bundle.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from botracked.infrastructure.gui.layout.slots import LayoutSlots

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LayoutSlotsTest(TestCase):
    '''
        Tests LayoutSlots attribute retention.
    '''

    def test_fields(self) -> None:
        '''
            Verifies central, mission, and cockpit slot frame retention.

            :exceptions: None.
        '''
        central = MagicMock(spec=Frame)
        mission = MagicMock(spec=Frame)
        cockpit = MagicMock(spec=Frame)
        slots = LayoutSlots(
            central_frame=central,
            mission_slot=mission,
            cockpit_slot=cockpit,
        )
        self.assertIs(slots.central_frame, central)
        self.assertIs(slots.mission_slot, mission)
        self.assertIs(slots.cockpit_slot, cockpit)


if __name__ == '__main__':
    main()
