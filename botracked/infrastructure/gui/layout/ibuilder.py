# -*- coding: UTF-8 -*-

'''
Module
    ibuilder.py
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
    Defines ILayoutBuilder protocol for mounting application panels.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Frame
from typing import Protocol, runtime_checkable

from botracked.infrastructure.gui.layout.bundle import GuiPanelsBundle
from botracked.infrastructure.gui.layout.slots import LayoutSlots

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class ILayoutBuilder(Protocol):
    '''
        Defines structural contract ILayoutBuilder for arranging GUI panels.

        It defines:

            :methods:
                | create_slots - Creates native split-pane parent containers.
                | mount_layout - Mounts primary panels into root window layout.
                | get_root - Returns root Tk window instance.
    '''

    def create_slots(self) -> LayoutSlots:
        '''
            Creates native split-pane parent containers for workspace panels.

            :return: LayoutSlots container bundle.
        '''

    def mount_layout(
        self, slots: LayoutSlots, panels: GuiPanelsBundle
    ) -> Frame:
        '''
            Mounts panels and arranges GUI layout hierarchy.

            :param slots: Native split-pane container frames bundle.
            :param panels: Bundle containing primary panel contracts.
            :return: Central split-pane Frame widget.
        '''

    def get_root(self) -> Tk:
        '''
            Returns root Tk window instance.

            :return: Root Tk window instance.
        '''
