# -*- coding: UTF-8 -*-

'''
Module
    jog_panel.py
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
    Provides JogPanel offering manual D-Pad control, PWM slider, and E-Stop.
'''

from __future__ import annotations

from tkinter import LEFT, RIGHT, X, DoubleVar, StringVar
from tkinter.ttk import Button, Frame, Label, Scale

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.controls.jog_panel_callbacks import (
    JogPanelCallbacks,
)
from botracked.infrastructure.gui.controls.jog_panel_config import (
    JogPanelConfig,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/botracked'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogPanel:
    '''
        Defines class JogPanel with attribute(s) and method(s).
        Interactive motion panel with D-Pad, speed regulation, and emergency stop.

        It defines:

            :attributes:
                | _frame - Main container Frame widget.
                | _callbacks - JogPanelCallbacks bundle holding action delegates.
                | _config - JogPanelConfig holding UI literals and layout tokens.
                | _speed_var - DoubleVar binding slider value.
                | _speed_label_var - StringVar binding formatted speed text.
            :methods:
                | __init__ - Initializes jog panel controls.
                | get_widget - Returns root Frame widget.
                | set_speed - Sets speed slider to requested PWM level.
                | get_current_speed - Returns current PWM speed setting.
                | bind_keyboard - Binds keyboard WASD/Q/E/Space hotkeys to window.
                | _build_ui - Constructs internal widget layout and D-Pad.
                | _handle_speed_slider - Handles slider drag events.
    '''

    _frame: Frame
    _callbacks: JogPanelCallbacks
    _config: JogPanelConfig
    _speed_var: DoubleVar
    _speed_label_var: StringVar

    def __init__(
        self,
        parent: Frame,
        callbacks: JogPanelCallbacks,
        config: JogPanelConfig | None = None,
    ) -> None:
        '''
            Initializes jog panel controls.

            :param parent: Parent Tk widget.
            :param callbacks: JogPanelCallbacks bundle holding action delegates.
            :param config: Optional JogPanelConfig instance.
            :exceptions: None.
        '''
        self._callbacks = callbacks
        self._config = config if config is not None else JogPanelConfig()
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

    def set_speed(self, speed: int) -> None:
        '''
            Sets speed slider to requested PWM level.

            :param speed: PWM integer level [0, 255].
            :exceptions: None.
        '''
        clamped: int = max(0, min(self._config.max_speed, speed))
        self._speed_var.set(float(clamped))
        self._handle_speed_slider(str(clamped))

    def get_current_speed(self) -> int:
        '''
            Returns current PWM speed setting.

            :return: Speed integer level.
            :exceptions: None.
        '''
        return int(self._speed_var.get())

    def bind_keyboard(self, root_widget: object) -> None:
        '''
            Binds keyboard WASD/Q/E/Space hotkeys to window.

            :param root_widget: Tk root window instance.
            :exceptions: None.
        '''
        if hasattr(root_widget, 'bind'):
            root_widget.bind('<w>', lambda _: self._callbacks.on_motion(MotionCommand.FORWARD))
            root_widget.bind('<s>', lambda _: self._callbacks.on_motion(MotionCommand.BACKWARD))
            root_widget.bind('<a>', lambda _: self._callbacks.on_motion(MotionCommand.TURN_LEFT))
            root_widget.bind('<d>', lambda _: self._callbacks.on_motion(MotionCommand.TURN_RIGHT))
            root_widget.bind('<q>', lambda _: self._callbacks.on_motion(MotionCommand.SPIN_LEFT))
            root_widget.bind('<e>', lambda _: self._callbacks.on_motion(MotionCommand.SPIN_RIGHT))
            root_widget.bind('<space>', lambda _: self._callbacks.on_stop())

    def _build_ui(self) -> None:
        '''
            Constructs internal widget layout and D-Pad.

            :exceptions: None.
        '''
        cfg: JogPanelConfig = self._config
        Label(self._frame, text=cfg.header_text, style='Header.TLabel').pack(anchor='w', pady=(0, 8))

        # Speed slider section
        slider_frame: Frame = Frame(self._frame, style='Surface.TFrame', padding=cfg.padding_section)
        slider_frame.pack(fill=X, pady=(0, 10))

        self._speed_var = DoubleVar(value=cfg.default_speed)
        self._speed_label_var = StringVar(value=f'Speed PWM: {int(cfg.default_speed)} (70%)')

        Label(slider_frame, textvariable=self._speed_label_var, style='CardTitle.TLabel').pack(anchor='w')
        slider: Scale = Scale(
            slider_frame,
            from_=0,
            to=cfg.max_speed,
            orient='horizontal',
            variable=self._speed_var,
            command=self._handle_speed_slider,
        )
        slider.pack(fill=X, pady=(4, 2))

        # D-Pad controls
        dpad: Frame = Frame(self._frame, style='Surface.TFrame', padding=cfg.padding_section)
        dpad.pack(pady=(0, 10))

        Button(
            dpad, text=cfg.spin_l_text, width=cfg.btn_width_dpad,
            command=lambda: self._callbacks.on_motion(MotionCommand.SPIN_LEFT),
        ).grid(row=0, column=0, padx=3, pady=3)
        Button(
            dpad, text=cfg.fwd_text, width=cfg.btn_width_center, style='Accent.TButton',
            command=lambda: self._callbacks.on_motion(MotionCommand.FORWARD),
        ).grid(row=0, column=1, padx=3, pady=3)
        Button(
            dpad, text=cfg.spin_r_text, width=cfg.btn_width_dpad,
            command=lambda: self._callbacks.on_motion(MotionCommand.SPIN_RIGHT),
        ).grid(row=0, column=2, padx=3, pady=3)

        Button(
            dpad, text=cfg.left_text, width=cfg.btn_width_dpad,
            command=lambda: self._callbacks.on_motion(MotionCommand.TURN_LEFT),
        ).grid(row=1, column=0, padx=3, pady=3)
        Button(
            dpad, text=cfg.stop_text, width=cfg.btn_width_center,
            command=self._callbacks.on_stop,
        ).grid(row=1, column=1, padx=3, pady=3)
        Button(
            dpad, text=cfg.right_text, width=cfg.btn_width_dpad,
            command=lambda: self._callbacks.on_motion(MotionCommand.TURN_RIGHT),
        ).grid(row=1, column=2, padx=3, pady=3)

        Button(
            dpad, text=cfg.bwd_text, width=cfg.btn_width_center,
            command=lambda: self._callbacks.on_motion(MotionCommand.BACKWARD),
        ).grid(row=2, column=1, padx=3, pady=3)

        # Action and emergency buttons
        actions: Frame = Frame(self._frame, style='Panel.TFrame')
        actions.pack(fill=X, pady=(4, 0))

        Button(actions, text=cfg.estop_text, style='Danger.TButton', command=self._callbacks.on_stop).pack(fill=X, pady=(0, 6))

        aux: Frame = Frame(actions, style='Panel.TFrame')
        aux.pack(fill=X)
        Button(aux, text=cfg.ping_text, command=self._callbacks.on_ping).pack(side=LEFT, expand=True, fill=X, padx=(0, 2))
        Button(aux, text=cfg.clear_err_text, command=self._callbacks.on_clear_err).pack(side=RIGHT, expand=True, fill=X, padx=(2, 0))

    def _handle_speed_slider(self, val_str: str) -> None:
        '''
            Handles speed slider drag events and updates speed label.

            :param val_str: String value from slider widget.
            :exceptions: None.
        '''
        try:
            val: int = int(float(val_str))
            pct: int = int((val / float(self._config.max_speed)) * 100)
            self._speed_label_var.set(f'Speed PWM: {val} ({pct}%)')
            self._callbacks.on_speed(val)
        except ValueError:
            pass
