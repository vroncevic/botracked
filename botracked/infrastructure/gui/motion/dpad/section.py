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
    Defines MotionDpadSection leaf UI component for manual robotics steering.
'''

from __future__ import annotations

from collections.abc import Mapping
from tkinter import Tk
from tkinter.ttk import Button, Frame
from typing import ClassVar

from botracked.core.model.motion_command import MotionCommand
from botracked.infrastructure.gui.motion.dpad.trigger.itrigger import IMotionTrigger
from botracked.infrastructure.gui.motion.idelegate import IMotionActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MotionDpadSection:
    '''
        Defines class MotionDpadSection implementing IMotionDpadSection.
        Leaf UI section presenting manual 3x3 steering D-Pad without lambdas.

        It defines:

            :attributes:
                | BTN_WIDTH - Uniform button character width.
                | GRID_PAD - Grid cell horizontal and vertical padding.
                | UNIFORM_GROUP - Grid uniform column group identifier.
                | STATE_NORMAL - Interactive ttk button state.
                | STATE_DISABLED - Disabled ttk button state.
                | _frame - Sub-container Frame widget.
                | _delegate - Motion action delegate port.
                | _buttons - Tuple of all nine grid Button widgets.
            :methods:
                | __init__ - Initializes D-pad buttons with bound triggers.
                | get_widget - Returns section container Frame widget.
                | trigger_motion - Dispatches locomotion command to delegate.
                | trigger_stop - Dispatches immediate halt to delegate.
                | set_enabled - Enables or disables steering buttons.
    '''

    BTN_WIDTH: ClassVar[int] = 6
    GRID_PAD: ClassVar[int] = 3
    UNIFORM_GROUP: ClassVar[str] = 'dpad_cols'
    STATE_NORMAL: ClassVar[str] = 'normal'
    STATE_DISABLED: ClassVar[str] = 'disabled'

    _frame: Frame
    _delegate: IMotionActionDelegate
    _buttons: tuple[Button, ...]

    def __init__(
        self,
        parent: Frame | Tk,
        delegate: IMotionActionDelegate,
        triggers: Mapping[MotionCommand, IMotionTrigger],
    ) -> None:
        '''
            Initializes D-pad buttons using injected IMotionTrigger objects.

            :param parent: Parent container widget.
            :param delegate: Motion action delegate port.
            :param triggers: Mapping of MotionCommand to IMotionTrigger ports.
            :exceptions: None.
        '''
        self._frame = Frame(parent, style='Panel.TFrame')
        self._delegate = delegate
        for col_i in (0, 1, 2):
            self._frame.columnconfigure(
                col_i, weight=1, uniform=self.UNIFORM_GROUP
            )

        grid_specs: tuple[tuple[str, int, int, str, object], ...] = (
            ('↺', 0, 0, 'TButton', triggers[MotionCommand.SPIN_LEFT].invoke),
            ('▲', 0, 1, 'TButton', triggers[MotionCommand.FORWARD].invoke),
            ('↻', 0, 2, 'TButton', triggers[MotionCommand.SPIN_RIGHT].invoke),
            ('◄', 1, 0, 'TButton', triggers[MotionCommand.TURN_LEFT].invoke),
            ('STOP', 1, 1, 'Danger.TButton', self.trigger_stop),
            ('►', 1, 2, 'TButton', triggers[MotionCommand.TURN_RIGHT].invoke),
            ('PING', 2, 0, 'TButton', delegate.handle_ping),
            ('▼', 2, 1, 'TButton', triggers[MotionCommand.BACKWARD].invoke),
            ('CLR', 2, 2, 'TButton', delegate.handle_clear_errors),
        )

        created: list[Button] = []
        for caption, row_idx, col_idx, style_name, action in grid_specs:
            btn = Button(
                self._frame,
                text=caption,
                style=style_name,
                width=self.BTN_WIDTH,
                command=action,
            )
            btn.grid(
                row=row_idx,
                column=col_idx,
                padx=self.GRID_PAD,
                pady=self.GRID_PAD,
                sticky='ew',
            )
            created.append(btn)

        self._buttons = tuple(created)

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def trigger_motion(self, cmd: MotionCommand) -> None:
        '''
            Dispatches locomotion command to delegate.

            :param cmd: MotionCommand enum.
            :exceptions: None.
        '''
        self._delegate.handle_motion(cmd)

    def trigger_stop(self) -> None:
        '''
            Dispatches immediate halt to delegate.

            :exceptions: None.
        '''
        self._delegate.handle_stop()

    def set_enabled(self, enabled: bool) -> None:
        '''
            Enables or disables steering buttons.

            :param enabled: True if interactive, False if disabled.
            :exceptions: None.
        '''
        state_str: str = self.STATE_NORMAL if enabled else self.STATE_DISABLED
        for btn in self._buttons:
            btn.configure(state=state_str)
