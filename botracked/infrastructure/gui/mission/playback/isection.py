# -*- coding: UTF-8 -*-

'''
Module
    isection.py
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
    Defines IMissionPlaybackSection protocol for playback controls leaf UI.
'''

from __future__ import annotations

from tkinter.ttk import Frame
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/botracked/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

@runtime_checkable
class IMissionPlaybackSection(Protocol):
    '''
        Defines structural contract IMissionPlaybackSection for execution bar.

        It defines:

            :methods:
                | get_widget - Returns section container Frame widget.
                | on_run - Validates, compiles, and starts mission execution.
                | on_pause - Pauses running mission execution.
                | on_resume - Resumes paused mission execution.
                | on_abort - Immediately aborts active mission execution.
    '''

    def get_widget(self) -> Frame:
        '''
            Returns section container Frame widget.

            :return: Section Frame widget.
        '''

    def on_run(self) -> None:
        '''
            Validates, compiles, and starts mission execution.
        '''

    def on_pause(self) -> None:
        '''
            Pauses running mission execution.
        '''

    def on_resume(self) -> None:
        '''
            Resumes paused mission execution.
        '''

    def on_abort(self) -> None:
        '''
            Immediately aborts active mission execution.
        '''
