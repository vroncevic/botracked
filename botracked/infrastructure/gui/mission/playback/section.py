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
    Provides MissionPlaybackSection leaf UI component for mission execution.
'''

from __future__ import annotations

from tkinter.ttk import Button, Frame
from typing import ClassVar

from botracked.core.model.exceptions.botracked_error import BotrackedError
from botracked.infrastructure.gui.mission.editor.isection import IMissionEditorSection
from botracked.infrastructure.gui.mission.idelegate import IMissionActionDelegate
from botracked.infrastructure.gui.mission.playback.dependencies import MissionPlaybackDependencies
from botracked.infrastructure.gui.mission.status.isection import IMissionStatusSection
from botracked.infrastructure.gui.theme.colors import UIColors

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionPlaybackSection:
    '''
        Defines class MissionPlaybackSection implementing
        IMissionPlaybackSection contract structurally.

        It defines:

            :attributes:
                | BTN_WIDTH - Uniform playback button character width.
                | BTN_PADX - Horizontal padding around playback buttons.
                | _frame - Section container Frame widget.
                | _delegate - Mission action delegate port.
                | _editor_section - Mission editor leaf section port.
                | _status_section - Mission status leaf section port.
            :methods:
                | __init__ - Initializes Run, Pause, Resume, and Abort buttons.
                | get_widget - Returns section container Frame widget.
                | on_run - Validates and launches mission routine.
                | on_pause - Pauses active mission routine.
                | on_resume - Resumes paused mission routine.
                | on_abort - Aborts active mission routine.
    '''

    BTN_WIDTH: ClassVar[int] = 0
    BTN_PADX: ClassVar[int] = 2

    _frame: Frame
    _delegate: IMissionActionDelegate
    _editor_section: IMissionEditorSection
    _status_section: IMissionStatusSection

    def __init__(self, dependencies: MissionPlaybackDependencies) -> None:
        '''
            Initializes Run, Pause, Resume, and Abort playback buttons.

            :param dependencies: Playback section collaborator ports bundle.
            :exceptions: None.
        '''
        self._frame = Frame(dependencies.parent, style='Panel.TFrame')
        self._delegate = dependencies.delegate
        self._editor_section = dependencies.editor_section
        self._status_section = dependencies.status_section

        specs: tuple[tuple[str, str, object], ...] = (
            ('▶ Run', 'Success.TButton', self.on_run),
            ('❚❚ Pause', 'TButton', self.on_pause),
            ('▶ Resume', 'Accent.TButton', self.on_resume),
            ('■ Abort', 'Danger.TButton', self.on_abort),
        )
        for col_idx, (label_text, style_name, action) in enumerate(specs):
            self._frame.columnconfigure(col_idx, weight=1)
            Button(
                self._frame,
                text=label_text,
                style=style_name,
                width=self.BTN_WIDTH,
                command=action,
            ).grid(row=0, column=col_idx, padx=self.BTN_PADX, sticky='ew')

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def on_run(self) -> None:
        '''
            Validates and launches mission routine execution.

            :exceptions: None.
        '''
        script: str = self._editor_section.get_script()
        is_valid, message = self._delegate.handle_validate(script)
        if not is_valid:
            self._status_section.set_status(message, str(UIColors.RED))
            return

        try:
            self._delegate.handle_run(script)
            self._status_section.set_status('Mission running', str(UIColors.GREEN))
        except BotrackedError as exc:
            self._status_section.set_status(
                f'Mission error: {exc}', str(UIColors.RED)
            )

    def on_pause(self) -> None:
        '''
            Pauses active mission routine execution.

            :exceptions: None.
        '''
        self._delegate.handle_pause()
        self._status_section.set_status('Mission paused', str(UIColors.AMBER))

    def on_resume(self) -> None:
        '''
            Resumes paused mission routine execution.

            :exceptions: None.
        '''
        self._delegate.handle_resume()
        self._status_section.set_status('Mission resumed', str(UIColors.GREEN))

    def on_abort(self) -> None:
        '''
            Aborts active mission routine execution.

            :exceptions: None.
        '''
        self._delegate.handle_abort()
        self._status_section.set_status('Mission aborted', str(UIColors.RED))
