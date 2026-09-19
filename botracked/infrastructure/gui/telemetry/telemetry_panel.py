# -*- coding: UTF-8 -*-

'''
Module
    telemetry_panel.py
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
    Provides TelemetryPanel displaying live robot operational metrics.
'''

from __future__ import annotations

from tkinter import BOTH, StringVar
from tkinter.ttk import Frame, Label

from botracked.core.model.telemetry_data import TelemetryData
from botracked.infrastructure.gui.telemetry.telemetry_panel_config import (
    TelemetryPanelConfig,
)
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TelemetryPanel:
    '''
        Live telemetry card grid displaying AVR system states, actuator
        directions, PWM levels, and diagnostic health.

        It defines:

            :attributes:
                | _frame - Root Frame widget.
                | _config - Configuration instance for telemetry panel.
                | _mode_var - StringVar holding current robot operating mode.
                | _motion_var - StringVar holding active motion command token.
                | _speed_var - StringVar holding current speed PWM level.
                | _left_motor_var - StringVar holding left motor state.
                | _right_motor_var - StringVar holding right motor state.
                | _err_var - StringVar holding diagnostic error code hex.
                | _uptime_var - StringVar holding robot uptime string.
                | _mode_lbl - Label widget for displaying robot operating mode.
            :methods:
                | __init__ - Initializes telemetry dashboard cards.
                | get_widget - Returns root Frame widget.
                | reset_telemetry - Resets all displayed telemetry values.
                | update_telemetry - Updates displayed card metrics.
    '''

    _frame: Frame
    _config: TelemetryPanelConfig
    _mode_var: StringVar
    _motion_var: StringVar
    _speed_var: StringVar
    _left_motor_var: StringVar
    _right_motor_var: StringVar
    _err_var: StringVar
    _uptime_var: StringVar
    _mode_lbl: Label

    def __init__(
        self, parent: Frame, config: TelemetryPanelConfig | None = None
    ) -> None:
        '''
            Initializes telemetry dashboard cards.

            :param parent: Parent Tk widget.
            :param config: Optional panel configuration instance.
            :exceptions: None.
        '''
        self._config = config if config is not None else TelemetryPanelConfig()
        self._frame = Frame(
            parent, style='Panel.TFrame', padding=self._config.padding_main
        )
        self._build_ui()

    def get_widget(self) -> Frame:
        '''
            Returns root Frame widget.

            :return: Frame instance.
            :exceptions: None.
        '''
        return self._frame

    def reset_telemetry(self) -> None:
        '''
            Resets all displayed telemetry values to default offline state.

            :exceptions: None.
        '''
        cfg: TelemetryPanelConfig = self._config
        self._mode_var.set(cfg.default_mode)
        self._mode_lbl.configure(foreground=UIColors.TEXT_MUTED)
        self._motion_var.set(cfg.default_motion)
        self._speed_var.set(cfg.default_speed)
        self._left_motor_var.set(cfg.default_motion)
        self._right_motor_var.set(cfg.default_motion)
        self._err_var.set(cfg.default_err)
        self._uptime_var.set(cfg.default_uptime)

    def update_telemetry(self, data: TelemetryData) -> None:
        '''
            Updates displayed card metrics from TelemetryData snapshot.

            :param data: TelemetryData instance.
            :exceptions: None.
        '''
        mode_str: str = data.mode_str
        self._mode_var.set(mode_str)
        if mode_str == 'NORMAL':
            self._mode_lbl.configure(foreground=UIColors.GREEN)
        elif mode_str == 'DEGRADED':
            self._mode_lbl.configure(foreground=UIColors.AMBER)
        else:
            self._mode_lbl.configure(foreground=UIColors.RED)

        self._motion_var.set(data.motion_cmd_str)
        self._speed_var.set(str(data.speed_pwm))
        self._left_motor_var.set(data.motor_left_str)
        self._right_motor_var.set(data.motor_right_str)
        self._err_var.set(f'0x{data.error_code:02X}')
        self._uptime_var.set(f'{data.uptime_ms / 1000.0:.1f}s')

    def _init_variables(self) -> None:
        '''
            Initializes bound UI string variables with defaults.

            :exceptions: None.
        '''
        cfg: TelemetryPanelConfig = self._config
        self._mode_var = StringVar(value=cfg.default_mode)
        self._motion_var = StringVar(value=cfg.default_motion)
        self._speed_var = StringVar(value=cfg.default_speed)
        self._left_motor_var = StringVar(value=cfg.default_motion)
        self._right_motor_var = StringVar(value=cfg.default_motion)
        self._err_var = StringVar(value=cfg.default_err)
        self._uptime_var = StringVar(value=cfg.default_uptime)

    def _build_cards(self, grid: Frame) -> None:
        '''
            Builds metric card widgets in layout grid.

            :param grid: Layout grid Frame widget.
            :exceptions: None.
        '''
        cfg: TelemetryPanelConfig = self._config
        self._mode_lbl = self._create_card(
            grid, (cfg.card_mode, self._mode_var, UIColors.TEXT_MUTED), (0, 0)
        )
        self._create_card(
            grid, (cfg.card_motion, self._motion_var, UIColors.CYAN), (0, 1)
        )
        self._create_card(
            grid, (cfg.card_left_motor, self._left_motor_var, UIColors.AMBER), (1, 0)
        )
        self._create_card(
            grid, (cfg.card_right_motor, self._right_motor_var, UIColors.AMBER), (1, 1)
        )
        self._create_card(
            grid, (cfg.card_speed, self._speed_var, UIColors.BLUE), (2, 0)
        )
        self._create_card(
            grid, (cfg.card_error, self._err_var, UIColors.RED), (2, 1)
        )
        self._create_card(
            grid,
            (cfg.card_uptime, self._uptime_var, UIColors.GREEN),
            (3, 0),
            colspan=2,
        )

    def _build_ui(self) -> None:
        '''
            Constructs internal telemetry cards and layout grid.

            :exceptions: None.
        '''
        cfg: TelemetryPanelConfig = self._config
        Label(self._frame, text=cfg.title_header, style='Header.TLabel').pack(
            anchor='w', pady=(0, 8)
        )
        grid: Frame = Frame(self._frame, style='Panel.TFrame')
        grid.pack(fill=BOTH, expand=True)

        self._init_variables()
        self._build_cards(grid)

    def _create_card(
        self,
        parent: Frame,
        spec: tuple[str, StringVar, str],
        pos: tuple[int, int],
        colspan: int = 1,
    ) -> Label:
        '''
            Helper for building an individual metric card.

            :param parent: Parent Frame widget.
            :param spec: Metric specification containing title, variable, color.
            :param pos: Grid row and column tuple (row, col).
            :param colspan: Optional column span.
            :return: Configured value Label widget.
            :exceptions: None.
        '''
        title, var, fg = spec
        row, col = pos
        card: Frame = Frame(
            parent, style='Surface.TFrame', padding=self._config.padding_card
        )
        card.grid(row=row, column=col, columnspan=colspan, padx=4, pady=4, sticky='nsew')
        parent.columnconfigure(col, weight=1)

        Label(card, text=title, style='CardTitle.TLabel').pack(anchor='w')
        val_lbl: Label = Label(card, textvariable=var, style='CardValue.TLabel', foreground=fg)
        val_lbl.pack(anchor='w', pady=(2, 0))
        return val_lbl
