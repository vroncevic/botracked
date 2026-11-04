# -*- coding: UTF-8 -*-

'''
Module
    section.py
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
    Defines TelemetryCardSection leaf UI component presenting status cards.
'''

from __future__ import annotations

from tkinter import StringVar, Tk
from tkinter.ttk import Frame, Label
from typing import ClassVar

from botracked.core.model.system_mode import SystemMode
from botracked.core.model.telemetry_data import TelemetryData
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

class TelemetryCardSection:
    '''
        Defines class TelemetryCardSection implementing ITelemetryCardSection.
        Leaf UI section presenting seven telemetry metric cards in a 2-col grid.

        It defines:

            :attributes:
                | CARD_PAD - Outer grid cell padding in pixels.
                | VALUE_PAD_TOP - Vertical gap above card value label.
                | MS_PER_SEC - Milliseconds per second divisor.
                | UNIFORM_GROUP - Grid uniform column group identifier.
                | _frame - Grid container Frame widget.
                | _config - Telemetry panel configuration value object.
                | _mode_var - Bound StringVar for operating mode.
                | _motion_var - Bound StringVar for motion state.
                | _left_var - Bound StringVar for left motor state.
                | _right_var - Bound StringVar for right motor state.
                | _speed_var - Bound StringVar for speed PWM.
                | _err_var - Bound StringVar for error code.
                | _uptime_var - Bound StringVar for robot uptime.
                | _mode_lbl - Label widget for colored mode badge.
            :methods:
                | __init__ - Initializes metric cards and grid layout.
                | get_widget - Returns section container Frame widget.
                | update_metrics - Updates card display values from data.
                | reset_metrics - Resets displayed cards to offline defaults.
                | get_mode_text - Returns current operating mode string.
    '''

    CARD_PAD: ClassVar[int] = 4
    VALUE_PAD_TOP: ClassVar[int] = 2
    MS_PER_SEC: ClassVar[float] = 1000.0
    UNIFORM_GROUP: ClassVar[str] = 'telem_cards'

    _frame: Frame
    _config: TelemetryPanelConfig
    _mode_var: StringVar
    _motion_var: StringVar
    _left_var: StringVar
    _right_var: StringVar
    _speed_var: StringVar
    _err_var: StringVar
    _uptime_var: StringVar
    _mode_lbl: Label

    def __init__(
        self,
        parent: Frame | Tk,
        config: TelemetryPanelConfig,
    ) -> None:
        '''
            Initializes metric cards and grid layout with explicit config.

            :param parent: Parent container widget.
            :param config: Telemetry configuration value object.
            :exceptions: None.
        '''
        self._config = config
        self._frame = Frame(parent, style='Panel.TFrame')

        self._mode_var = StringVar(value=config.default_mode)
        self._motion_var = StringVar(value=config.default_motion)
        self._left_var = StringVar(value=config.default_motion)
        self._right_var = StringVar(value=config.default_motion)
        self._speed_var = StringVar(value=config.default_speed)
        self._err_var = StringVar(value=config.default_err)
        self._uptime_var = StringVar(value=config.default_uptime)

        for col in (0, 1):
            self._frame.columnconfigure(
                col, weight=1, uniform=self.UNIFORM_GROUP
            )

        card_mode = Frame(
            self._frame, style='Surface.TFrame', padding=config.padding_card
        )
        card_mode.grid(
            row=0, column=0, padx=self.CARD_PAD, pady=self.CARD_PAD, sticky='nsew'
        )
        Label(card_mode, text=config.card_mode, style='CardTitle.TLabel').pack(
            fill='x', anchor='w'
        )
        self._mode_lbl = Label(
            card_mode, textvariable=self._mode_var, style='CardValue.TLabel'
        )
        self._mode_lbl.pack(
            fill='x', anchor='w', pady=(self.VALUE_PAD_TOP, 0)
        )

        specs: tuple[tuple[str, StringVar, int, int, int], ...] = (
            (config.card_motion, self._motion_var, 0, 1, 1),
            (config.card_left_motor, self._left_var, 1, 0, 1),
            (config.card_right_motor, self._right_var, 1, 1, 1),
            (config.card_speed, self._speed_var, 2, 0, 1),
            (config.card_error, self._err_var, 2, 1, 1),
            (config.card_uptime, self._uptime_var, 3, 0, 2),
        )
        for title_txt, bound_var, r_idx, c_idx, c_span in specs:
            card = Frame(
                self._frame,
                style='Surface.TFrame',
                padding=config.padding_card,
            )
            card.grid(
                row=r_idx,
                column=c_idx,
                columnspan=c_span,
                padx=self.CARD_PAD,
                pady=self.CARD_PAD,
                sticky='nsew',
            )
            Label(card, text=title_txt, style='CardTitle.TLabel').pack(
                fill='x', anchor='w'
            )
            Label(card, textvariable=bound_var, style='CardValue.TLabel').pack(
                fill='x', anchor='w', pady=(self.VALUE_PAD_TOP, 0)
            )

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def update_metrics(self, data: TelemetryData) -> None:
        '''
            Updates card display values from TelemetryData snapshot.

            :param data: TelemetryData instance.
            :exceptions: None.
        '''
        mode_str: str = data.system_mode
        self._mode_var.set(mode_str)
        match mode_str:
            case SystemMode.NORMAL:
                self._mode_lbl.configure(foreground=UIColors.GREEN)
            case SystemMode.DEGRADED:
                self._mode_lbl.configure(foreground=UIColors.AMBER)
            case _:
                self._mode_lbl.configure(foreground=UIColors.RED)

        self._motion_var.set(data.motion.name.replace('_', ' '))
        self._left_var.set(data.left_motor_state)
        self._right_var.set(data.right_motor_state)
        self._speed_var.set(str(data.speed_pwm))
        self._err_var.set(f'0x{data.error_code:02X}')
        self._uptime_var.set(f'{data.uptime_ms / self.MS_PER_SEC:.1f}s')

    def reset_metrics(self) -> None:
        '''
            Resets displayed cards to offline defaults.

            :exceptions: None.
        '''
        cfg: TelemetryPanelConfig = self._config
        self._mode_var.set(cfg.default_mode)
        self._mode_lbl.configure(foreground=UIColors.TEXT_MUTED)
        self._motion_var.set(cfg.default_motion)
        self._left_var.set(cfg.default_motion)
        self._right_var.set(cfg.default_motion)
        self._speed_var.set(cfg.default_speed)
        self._err_var.set(cfg.default_err)
        self._uptime_var.set(cfg.default_uptime)

    def get_mode_text(self) -> str:
        '''
            Returns current operating mode string.

            :return: Current mode string.
            :exceptions: None.
        '''
        return self._mode_var.get()
