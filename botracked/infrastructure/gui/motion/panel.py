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
    Provides MotionPanel composite UI component managing steering and speed.
'''

from __future__ import annotations

from tkinter import TOP, Tk, X
from tkinter.ttk import Frame, Label
from typing import ClassVar

from botracked.infrastructure.gui.motion.dependencies import MotionPanelDependencies
from botracked.infrastructure.gui.motion.dpad.isection import IMotionDpadSection
from botracked.infrastructure.gui.motion.keyboard.controller.icontroller import (
    IMotionKeyboardController,
)
from botracked.infrastructure.gui.motion.speed.isection import IMotionSpeedSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionPanel:
    '''
        Defines class MotionPanel implementing IMotionPanel contract.
        Composite UI component orchestrating D-pad, speed slider, and hotkeys.

        It defines:

            :attributes:
                | HEADER_TEXT - Panel title caption.
                | SECTION_PADX - Horizontal padding around child sections.
                | SECTION_PADY - Vertical padding around child sections.
                | _frame - Main container Frame widget.
                | _dpad_section - Injected manual steering D-pad section port.
                | _speed_section - Injected PWM speed slider section port.
                | _keyboard_controller - Injected hotkey controller port.
            :methods:
                | __init__ - Initializes motion panel with injected sections.
                | get_widget - Returns root container Frame widget.
                | get_speed - Returns current PWM speed integer value.
                | set_speed - Updates locomotion PWM speed setting.
                | set_enabled - Enables or disables motion controls.
                | bind_keyboard - Binds keyboard WASD and Space hotkeys.
    '''

    HEADER_TEXT: ClassVar[str] = 'MANUAL LOCOMOTION COCKPIT'
    SECTION_PADX: ClassVar[int] = 6
    SECTION_PADY: ClassVar[int] = 4

    _frame: Frame
    _dpad_section: IMotionDpadSection
    _speed_section: IMotionSpeedSection
    _keyboard_controller: IMotionKeyboardController

    def __init__(self, dependencies: MotionPanelDependencies) -> None:
        '''
            Initializes motion panel and mounts injected sub-sections.

            :param dependencies: Motion panel collaborator ports bundle.
            :exceptions: None.
        '''
        self._frame = dependencies.frame
        self._dpad_section = dependencies.dpad_section
        self._speed_section = dependencies.speed_section
        self._keyboard_controller = dependencies.keyboard_controller

        Label(
            self._frame,
            text=self.HEADER_TEXT,
            style='PanelHeader.TLabel',
        ).pack(side=TOP, fill=X, anchor='w', pady=(0, self.SECTION_PADY))

        self._dpad_section.get_widget().pack(
            in_=self._frame,
            side=TOP,
            fill=X,
            padx=self.SECTION_PADX,
            pady=self.SECTION_PADY,
        )
        self._speed_section.get_widget().pack(
            in_=self._frame,
            side=TOP,
            fill=X,
            padx=self.SECTION_PADX,
            pady=self.SECTION_PADY,
        )

    def get_widget(self) -> Frame:
        '''
            Returns root container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_speed(self) -> int:
        '''
            Returns current PWM speed integer value.

            :return: Current speed integer.
            :exceptions: None.
        '''
        return self._speed_section.get_speed()

    def set_speed(self, speed: int) -> None:
        '''
            Updates locomotion PWM speed setting.

            :param speed: New PWM speed integer.
            :exceptions: None.
        '''
        self._speed_section.set_speed(speed)

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables motion controls and keyboard teleoperation.

            :param enabled: True if interactive, False if disabled.
            :exceptions: None.
        '''
        self._dpad_section.set_enabled(enabled)
        self._speed_section.set_enabled(enabled)
        self._keyboard_controller.set_enabled(enabled)

    def bind_keyboard(self, window: Frame | Tk) -> None:
        '''
            Binds keyboard WASD and Space hotkeys to target window.

            :param window: Target frame or root window to bind.
            :exceptions: None.
        '''
        self._keyboard_controller.bind_to(window)
