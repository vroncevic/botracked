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
    Provides MissionToolbarSection composite mounting preset and playback.
'''

from __future__ import annotations

from tkinter import LEFT, X
from tkinter.ttk import Frame
from typing import ClassVar

from botracked.infrastructure.gui.mission.playback.isection import IMissionPlaybackSection
from botracked.infrastructure.gui.mission.preset.isection import IMissionPresetSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

class MissionToolbarSection:
    '''
        Defines class MissionToolbarSection implementing IMissionToolbarSection.
        Composite toolbar mounting injected preset and playback leaf sections.

        It defines:

            :attributes:
                | SECTION_GAP - Horizontal gap between preset and playback bars.
                | _frame - Container Frame widget.
                | _preset_section - Injected preset selector leaf section port.
                | _playback_section - Injected playback leaf section port.
            :methods:
                | __init__ - Mounts injected preset and playback leaf sections.
                | get_widget - Returns container Frame widget.
                | get_preset_section - Returns preset leaf section port.
                | get_playback_section - Returns playback leaf section port.
    '''

    SECTION_GAP: ClassVar[int] = 6

    _frame: Frame
    _preset_section: IMissionPresetSection
    _playback_section: IMissionPlaybackSection

    def __init__(
        self,
        frame: Frame,
        preset_section: IMissionPresetSection,
        playback_section: IMissionPlaybackSection,
    ) -> None:
        '''
            Mounts injected preset and playback leaf sections into toolbar.

            :param frame: Container Frame widget.
            :param preset_section: Injected preset selector leaf section.
            :param playback_section: Injected playback controls leaf section.
            :exceptions: None.
        '''
        self._frame = frame
        self._preset_section = preset_section
        self._playback_section = playback_section

        self._preset_section.get_widget().pack(
            in_=self._frame, side=LEFT, padx=(0, self.SECTION_GAP)
        )
        self._playback_section.get_widget().pack(
            in_=self._frame, side=LEFT, fill=X, expand=True
        )

    def get_widget(self) -> Frame:
        '''
            Returns container Frame widget.

            :return: Toolbar Frame widget.
            :exceptions: None.
        '''
        return self._frame

    def get_preset_section(self) -> IMissionPresetSection:
        '''
            Returns internal preset selector leaf section port.

            :return: IMissionPresetSection instance.
            :exceptions: None.
        '''
        return self._preset_section

    def get_playback_section(self) -> IMissionPlaybackSection:
        '''
            Returns internal playback controls leaf section port.

            :return: IMissionPlaybackSection instance.
            :exceptions: None.
        '''
        return self._playback_section
