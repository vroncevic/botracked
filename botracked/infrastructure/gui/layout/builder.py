# -*- coding: UTF-8 -*-

'''
Module
    builder.py
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
    Provides LayoutBuilder arranging primary GUI panels across root window.
'''

from __future__ import annotations

from tkinter import BOTH, BOTTOM, TOP, X, Tk
from tkinter.ttk import Frame
from typing import ClassVar

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

class LayoutBuilder:
    '''
        Defines class LayoutBuilder implementing ILayoutBuilder.
        Mounts connection, cockpit, mission, and console panels natively.

        It defines:

            :attributes:
                | PANEL_STYLE - Styled ttk frame name for split panes.
                | EDGE_PAD - Standard divider gap between panes in pixels.
                | COCKPIT_GAP - Vertical gap between motion and telemetry panels.
                | MISSION_WEIGHT - Grid column weight for left mission studio.
                | COCKPIT_WEIGHT - Grid column weight for right cockpit column.
                | COCKPIT_MINSIZE - Minimum pixel width for right cockpit pane.
                | _root - Root Tk window instance.
            :methods:
                | __init__ - Initializes layout builder with root window.
                | create_slots - Creates native split-pane parent containers.
                | mount_layout - Mounts panels and arranges GUI layout hierarchy.
                | get_root - Returns root Tk window instance.
    '''

    PANEL_STYLE: ClassVar[str] = 'TFrame'
    EDGE_PAD: ClassVar[int] = 4
    COCKPIT_GAP: ClassVar[int] = 4
    MISSION_WEIGHT: ClassVar[int] = 5
    COCKPIT_WEIGHT: ClassVar[int] = 2
    COCKPIT_MINSIZE: ClassVar[int] = 400

    _root: Tk

    def __init__(self, root: Tk) -> None:
        '''
            Initializes layout builder with root window.

            :param root: Root Tk window instance.
            :exceptions: None.
        '''
        self._root = root

    def create_slots(self) -> LayoutSlots:
        '''
            Creates native split-pane parent containers for workspace panels.

            :return: LayoutSlots container bundle.
            :exceptions: None.
        '''
        central_frame = Frame(self._root, style=self.PANEL_STYLE)
        mission_slot = Frame(central_frame, style=self.PANEL_STYLE)
        cockpit_slot = Frame(central_frame, style=self.PANEL_STYLE)

        return LayoutSlots(
            central_frame=central_frame,
            mission_slot=mission_slot,
            cockpit_slot=cockpit_slot,
        )

    def mount_layout(
        self, slots: LayoutSlots, panels: GuiPanelsBundle
    ) -> Frame:
        '''
            Mounts panels and arranges GUI layout hierarchy natively.

            :param slots: Native split-pane container frames bundle.
            :param panels: Parameter bundle containing all panel contracts.
            :return: Central frame holding split panes.
            :exceptions: None.
        '''
        panels.connection.get_widget().pack(
            fill=X, side=TOP, pady=(0, self.EDGE_PAD)
        )
        panels.console.get_widget().pack(
            fill=X, side=BOTTOM, pady=(self.EDGE_PAD, 0)
        )

        slots.central_frame.pack(fill=BOTH, expand=True)
        slots.central_frame.rowconfigure(0, weight=1)
        slots.central_frame.columnconfigure(0, weight=self.MISSION_WEIGHT)
        slots.central_frame.columnconfigure(
            1, weight=self.COCKPIT_WEIGHT, minsize=self.COCKPIT_MINSIZE
        )

        slots.mission_slot.grid(
            row=0, column=0, sticky='nsew', padx=(0, self.EDGE_PAD)
        )
        panels.mission.get_widget().pack(fill=BOTH, expand=True)

        slots.cockpit_slot.grid(
            row=0, column=1, sticky='nsew', padx=(self.EDGE_PAD, 0)
        )
        panels.motion.get_widget().pack(
            fill=X, side=TOP, pady=(0, self.COCKPIT_GAP)
        )
        panels.telemetry.get_widget().pack(
            fill=BOTH, expand=True, side=TOP
        )

        return slots.central_frame

    def get_root(self) -> Tk:
        '''
            Returns root Tk window instance.

            :return: Tk root instance.
            :exceptions: None.
        '''
        return self._root
