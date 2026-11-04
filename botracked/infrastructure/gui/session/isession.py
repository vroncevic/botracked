# -*- coding: UTF-8 -*-

'''
Module
    isession.py
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
    Defines IGuiSession protocol representing an active mounted GUI session.
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
class IGuiSession(Protocol):
    '''
        Defines structural contract IGuiSession for an active Tk GUI session.

        It defines:

            :methods:
                | set_script - Updates mission script text in active editor.
                | start - Enters main GUI event loop.
                | stop - Stops active session and releases resources.
    '''

    def set_script(self, script_text: str) -> None:
        '''
            Updates mission script text in active editor.

            :param script_text: Raw .track script content.
        '''

    def start(self) -> None:
        '''
            Enters main GUI event loop.
        '''

    def stop(self) -> None:
        '''
            Stops active session and releases resources.
        '''
