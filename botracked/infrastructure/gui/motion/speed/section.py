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
    Defines MotionSpeedSection leaf UI component for PWM speed regulation.
'''

from __future__ import annotations

from tkinter import DoubleVar, StringVar, Tk
from tkinter.ttk import Frame, Label, Scale
from typing import ClassVar

from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionSpeedSection:
    '''
        Defines class MotionSpeedSection implementing IMotionSpeedSection.
        Leaf UI section presenting locomotion PWM speed slider and readout.

        It defines:

            :attributes:
                | MIN_SPEED - Minimum PWM duty integer.
                | MAX_SPEED - Maximum PWM duty integer.
                | FALLBACK_SPEED - Fallback speed if slider string is malformed.
                | SCALE_LENGTH - Slider pixel width.
                | VALUE_WIDTH - Readout label character width.
                | WIDGET_PADX - Horizontal padding around child widgets.
                | SLIDER_WEIGHT - Grid column weight for slider widget.
                | STATE_NORMAL - Interactive widget state string.
                | STATE_DISABLED - Disabled widget state string.
                | _frame - Sub-container Frame widget.
                | _delegate - Motion action delegate port.
                | _speed_var - Bound DoubleVar for slider value.
                | _speed_label_var - Bound StringVar for formatted speed text.
                | _scale - Scale widget for PWM level regulation.
            :methods:
                | __init__ - Initializes speed section controls.
                | get_widget - Returns section container Frame widget.
                | get_speed - Returns current PWM speed integer value.
                | set_speed - Updates slider to requested PWM level.
                | on_slider_change - Handles slider drag interaction.
                | set_enabled - Enables or disables speed slider control.
    '''

    MIN_SPEED: ClassVar[int] = 0
    MAX_SPEED: ClassVar[int] = 255
    FALLBACK_SPEED: ClassVar[int] = 150
    SCALE_LENGTH: ClassVar[int] = 160
    VALUE_WIDTH: ClassVar[int] = 4
    WIDGET_PADX: ClassVar[int] = 4
    SLIDER_WEIGHT: ClassVar[int] = 6
    STATE_NORMAL: ClassVar[str] = 'normal'
    STATE_DISABLED: ClassVar[str] = 'disabled'

    _frame: Frame
    _delegate: IMotionActionDelegate
    _speed_var: DoubleVar
    _speed_label_var: StringVar
    _scale: Scale

    def __init__(
        self,
        parent: Frame | Tk,
        delegate: IMotionActionDelegate,
        default_speed: int,
    ) -> None:
        '''
            Initializes speed section controls without default magic parameters.

            :param parent: Parent container widget.
            :param delegate: Motion action delegate port.
            :param default_speed: Initial PWM speed integer between 0 and 255.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Panel.TFrame')
        self._delegate = delegate
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=self.SLIDER_WEIGHT)
        self._frame.columnconfigure(2, weight=1)

        clamped_init = max(self.MIN_SPEED, min(self.MAX_SPEED, default_speed))
        self._speed_var = DoubleVar(value=float(clamped_init))
        self._speed_label_var = StringVar(value=f'{clamped_init}')

        lbl = Label(
            self._frame, text='Speed:', style='Panel.TLabel', anchor='w'
        )
        lbl.grid(row=0, column=0, sticky='ew', padx=self.WIDGET_PADX)

        self._scale = Scale(
            self._frame,
            from_=self.MIN_SPEED,
            to=self.MAX_SPEED,
            orient='horizontal',
            variable=self._speed_var,
            command=self.on_slider_change,
            length=self.SCALE_LENGTH,
        )
        self._scale.grid(row=0, column=1, sticky='ew', padx=self.WIDGET_PADX)

        val_lbl = Label(
            self._frame,
            textvariable=self._speed_label_var,
            style='Panel.TLabel',
            anchor='e',
            width=self.VALUE_WIDTH,
        )
        val_lbl.grid(row=0, column=2, sticky='ew', padx=self.WIDGET_PADX)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_speed(self) -> int:
        '''
            Returns current PWM speed integer value.

            :return: Speed integer between 0 and 255.
            :exceptions: None.
        '''
        return int(round(self._speed_var.get()))

    def set_speed(self, speed: int) -> None:
        '''
            Updates slider to requested PWM level.

            :param speed: New PWM speed integer.
            :exceptions: None.
        '''
        clamped: int = max(self.MIN_SPEED, min(self.MAX_SPEED, speed))
        self._speed_var.set(float(clamped))
        self._speed_label_var.set(f'{clamped}')

    def on_slider_change(self, value: str) -> None:
        '''
            Handles slider drag interaction.

            :param value: Scale value string from Tkinter callback.
            :exceptions: None.
        '''
        try:
            raw_int: int = int(round(float(value)))
        except ValueError:
            raw_int = self.FALLBACK_SPEED
        speed_int: int = max(self.MIN_SPEED, min(self.MAX_SPEED, raw_int))
        self._speed_var.set(float(speed_int))
        self._speed_label_var.set(f'{speed_int}')
        self._delegate.handle_speed(speed_int)

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables speed slider control.

            :param enabled: True if interactive, False if disabled.
            :exceptions: None.
        '''
        state_str: str = self.STATE_NORMAL if enabled else self.STATE_DISABLED
        self._scale.configure(state=state_str)
