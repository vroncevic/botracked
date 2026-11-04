# -*- coding: UTF-8 -*-

'''
Module
    panel.py
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
    Defines TelemetryPanel composite UI component implementing ITelemetryPanel.
'''

from __future__ import annotations

from tkinter import BOTH, StringVar
from tkinter.ttk import Frame, Label
from typing import ClassVar

from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.telemetry.card.isection import ITelemetryCardSection
from botracked.infrastructure.gui.telemetry.config import TelemetryPanelConfig
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class TelemetryPanel:
    '''
        Defines class TelemetryPanel implementing ITelemetryPanel and
        ITelemetryView contracts structurally.

        It defines:

            :attributes:
                | INITIAL_PKTS - Initial packet counter badge text.
                | HEADER_GAP - Bottom padding below header row.
                | _frame - Root container Frame widget.
                | _card_section - Injected ITelemetryCardSection port.
                | _packet_var - Bound StringVar for packet counter.
            :methods:
                | __init__ - Initializes composite telemetry panel.
                | get_widget - Returns root container Frame widget.
                | update_telemetry - Updates metric cards with latest data.
                | update_packet_count - Updates total packet activity counter.
                | reset_telemetry - Resets metrics and packet counter.
    '''

    INITIAL_PKTS: ClassVar[str] = 'Pkts: 0'
    HEADER_GAP: ClassVar[int] = 6

    _frame: Frame
    _card_section: ITelemetryCardSection
    _packet_var: StringVar

    def __init__(
        self,
        frame: Frame,
        card_section: ITelemetryCardSection,
        config: TelemetryPanelConfig,
    ) -> None:
        '''
            Initializes composite telemetry panel with injected card section.

            :param frame: Root container Frame widget.
            :param card_section: Injected telemetry card section port.
            :param config: Telemetry panel configuration value object.
            :exceptions: None.
        '''
        self._frame = frame
        self._card_section = card_section
        self._packet_var = StringVar(value=self.INITIAL_PKTS)

        header_frame = Frame(self._frame, style='Panel.TFrame')
        header_frame.pack(fill='x', pady=(0, self.HEADER_GAP))

        packet_lbl = Label(
            header_frame,
            textvariable=self._packet_var,
            style='Panel.TLabel',
            foreground=UIColors.TEXT_MUTED,
        )
        packet_lbl.pack(side='right', anchor='e')

        title_lbl = Label(
            header_frame,
            text=config.title_header,
            style='PanelHeader.TLabel',
            anchor='w',
        )
        title_lbl.pack(side='left', fill='x', expand=True, anchor='w')

        self._card_section.get_widget().pack(
            in_=self._frame, fill=BOTH, expand=True
        )

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Root container Frame.
            :exceptions: None.
        '''
        return self._frame

    def update_telemetry(self, data: TelemetryData) -> None:
        '''
            Updates metric cards with latest telemetry data.

            :param data: Immutable TelemetryData snapshot.
            :exceptions: None.
        '''
        self._card_section.update_metrics(data)

    def update_packet_count(self, count: int) -> None:
        '''
            Updates total packet activity counter.

            :param count: Total packet count integer.
            :exceptions: None.
        '''
        self._packet_var.set(f'Pkts: {count}')

    def reset_telemetry(self) -> None:
        '''
            Resets metrics and packet counter to offline defaults.

            :exceptions: None.
        '''
        self._card_section.reset_metrics()
        self._packet_var.set(self.INITIAL_PKTS)
