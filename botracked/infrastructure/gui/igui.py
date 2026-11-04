# -*- coding: UTF-8 -*-

'''
Module
    igui.py
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
    Defines IGUI inbound presentation port for botracked GUI studio.
'''

from __future__ import annotations

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
class IGUI(Protocol):
    '''
        Defines structural contract IGUI for GUI studio presentation adapter.

        It defines:

            :methods:
                | is_initialized - Checks if GUI adapter is initialized.
                | load_script - Preloads or sets mission script text in studio.
                | start - Launches GUI cockpit and mission studio event loop.
                | stop - Terminates active GUI session and hardware links.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if GUI adapter is initialized and ready.

            :return: True if initialized, False otherwise.
        '''

    def load_script(self, script_text: str) -> None:
        '''
            Preloads or sets mission script text in studio editor.

            :param script_text: Raw .track mission script source text.
        '''

    def start(self) -> None:
        '''
            Launches GUI cockpit and mission studio event loop.
        '''

    def stop(self) -> None:
        '''
            Terminates active GUI session and hardware links.
        '''
